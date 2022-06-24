import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
from geopy.distance import geodesic as GD
from simulation.messages.cam import CAM, PublicTransportContainer, SpecialVehicle
from simulation.messages.denm import *
from threading import Thread
from sty import bg


class OBU:
    def __init__(self, name, id, address, length, width, navigation, speed):
        self.name = name
        self.id = id
        self.address = address
        self.length = length
        self.width = width
        self.state = "Gathering Info"
        self.speed = speed
        self.finished = False
        self.navigation = navigation
        self.coords = self.navigation.get_coords(self.speed)
        # By default, we start the simulation assuming the cars are involved
        self.other_cars = {}
        self.involved = True
        self.evaluated_inter = False
        self.lane_ending = False
        self.new_space = None
        self.bl = None
        self.fl = None
        self.adj_route = None
        self.helping_merge = False
        self.cams = 0

    def set_coords_and_position(self, values):
        self.position = values[0]
        self.coords = values[1]

    def set_state(self, state):
        self.state = state

    def set_speed(self, speed):
        self.speed = speed

    def set_finished(self, finished):
        self.finished = finished

    def accelerate(self):
        self.speed += 1
        print(bg.blue + "OBU[{n}] is Accelerating".format(n=self.id) + bg.rs)
        # Send a DENM about this decrease of speed
        denm_message = self.generate_denm(self.coords, CauseCode.speeding_up.value, 0)
        self.send_message("vanetza/in/denm", denm_message)
        pass

    def decelerate(self):
        # Decrease this OBU's speed by 3
        self.speed -= 3
        print(bg.blue + "OBU[{n}] is decelerating".format(n=self.id) + bg.rs)
        # Send a DENM about this decrease of speed
        denm_message = self.generate_denm(self.coords, CauseCode.breaking.value, 0)
        self.send_message("vanetza/in/denm", denm_message)

    def get_distance(self):
        pass

    def send_message(self, topic, message):
        publish.single(topic, json.dumps(message), hostname=self.address)

    def decide_next_move(self):
        pass

    def in_own_route(self, coordinates):
        if coordinates in self.navigation.current_route.coords:
            return True
        else:
            return False

    def has_space(self, new_route):
        # Get the space that the car needs in the new route
        # This is given by the position he wants to be in, minus/plus his width
        space_for_merge = self.navigation.space_between(self.new_space, new_route, self.length)
        # The back and forward limits of the zone we're checking
        self.bl = space_for_merge[0]
        self.fl = space_for_merge[-1]
        in_space = False
        cars_inside = []

        for car_id, stats in self.other_cars.items():
            # Check if the car in the new route we want to be in
            if self.navigation.check_in_route(new_route, stats['lon']):
                # Check if the car is in the space we want to be in
                if self.navigation.check_in_between(space_for_merge, (stats['lat'], stats['lon'])):
                    print(bg.red + "OBU[{n}] is in the space we want to be in".format(n=car_id) + bg.rs)
                    in_space = True
                    cars_inside.append(car_id)
                else:
                    print("OBU[{n}] checking".format(n=self.id))
                    print(bg.blue + "OBU[{n}] is NOT the space we want to be in".format(n=car_id) + bg.rs)
        return not in_space, cars_inside

    def merge(self):
        self.navigation.set_route(self.adj_route.name)
        # Set the new position in the new route
        # Still hardcoded, has to be cleaned up
        self.navigation.set_position(self.navigation.position + 5)

        # Send a message aboout the merge that has just finished
        denm_message = self.generate_denm(self.coords, CauseCode.merge_event.value, SubCauseCode.finished_merge.value)
        self.send_message("vanetza/in/denm", denm_message)

    def handle_message(self, client, userdata, message):
        msg_type = message.topic
        message = json.loads(message.payload)

        if msg_type == "vanetza/out/cam":
            cam_message = CAM.from_dict(message)
            si = cam_message.station_id
            speed = cam_message.speed
            lat = cam_message.latitude
            lon = cam_message.longitude
            self.update_road_state(si, lat, lon, speed)
            self.cams += 1

        if msg_type == "vanetza/out/denm":
            station_id = message["fields"]["denm"]["management"]["actionID"]["originatingStationID"]
            cause_code = message["fields"]["denm"]["situation"]["eventType"]["causeCode"]
            sub_cause_code = message["fields"]["denm"]["situation"]["eventType"]["subCauseCode"]
            lat = message["fields"]["denm"]["management"]["eventPosition"]["latitude"]
            lon = message["fields"]["denm"]["management"]["eventPosition"]["longitude"]

            # Check from cause code and sub cause code what type of situation it is
            if cause_code == 31 and self.involved:
                if sub_cause_code == 36:
                    print("OBU[{n}] Evaluating Merge Request from OBU[{n2}]".format(n=self.id, n2=station_id))
                    self.state = "Evaluating Merge"

                    # Check if this car is ahead or behind the merge location
                    if self.navigation.is_behind((lat, lon), self.coords):
                        print(bg.red + "OBU[{n}] Merge pont is behind".format(n=self.id) + bg.rs)
                        denm_message = self.generate_denm(self.coords, CauseCode.merge_event.value, SubCauseCode.not_involved.value)
                        self.send_message("vanetza/in/denm", denm_message)
                        # This car is not involved in the merge
                        self.involved = False
                        # Since this OBU is not involved, he goes to the
                        # First state
                        self.state = "Gathering Information"
                    else:
                        # Do Stuff
                        print(bg.blue + "OBU[{n}] Merge pont is ahead".format(n=self.id) + bg.rs)
                        self.involved = True
                        self.helping_merge = True

                if sub_cause_code == 37:
                    pass

                if sub_cause_code == 38:
                    # Means that the merge has ended, so the "involved flag" can
                    # be set off
                    self.involved = False
                    self.state = "Gathering Information"

                if sub_cause_code == 39:
                    print("OBU[{n}] | OBU[{n2}] stated that he is not involved".format(n=self.id, n2=station_id))
                    # Update our internal state for this OBU as not involved
                    for car_id in self.other_cars.keys():
                        if car_id == station_id:
                            self.other_cars[station_id]['involved'] = 'no'

            elif cause_code == 32:
                pass

            elif cause_code == 33:
                pass

            elif cause_code == 34:
                pass

            elif cause_code == 35 and (not self.evaluated_inter):
                self.evaluated_inter = True
                # it's an intersection denm
                # print("Check if intersection point is in own route")
                if self.in_own_route((lat, lon)):
                    print("In my route | OBU {n}".format(n=self.id))
                    self.involved = True
                    self.lane_ending = True
                    self.navigation.intersection = (lat, lon)

    def start(self):
        print("OBU[{n}] started".format(n=self.id))
        client = mqtt.Client(self.name)
        client.connect(self.address)
        client.on_message = self.handle_message
        client.loop_start()
        client.subscribe(topic=[("vanetza/out/denm", 0), ("vanetza/out/cam", 0)])
        started_merge = False

        while not self.finished:
            # update cars position
            self.coords, end = self.navigation.get_coords(self.speed)
            cam_message = self.generate_cam()
            self.send_message("vanetza/in/cam", cam_message)


            # If this OBU's lane is ending, check it's distance to the intersection
            if self.lane_ending is True:
                distance = round(GD(self.coords, self.navigation.intersection).m, 3)
                print("Distance to the intersection = {d}".format(d=distance))

                # If distance to the intersectiion is less than 60m, we send a DENM about the merge request
                if distance < 40 or started_merge:

                    # We only want to send a DENM once and only calculate the adj route once as well
                    if not started_merge:
                        started_merge = True
                        self.state = "Evaluating Merge"
                        # If the merge has started, we send a message indicating so
                        self.adj_route = self.navigation.get_adj_route()
                        new_space = self.navigation.get_merge_location(self.adj_route)
                        denm_message = self.generate_denm(new_space, CauseCode.merge_event.value, SubCauseCode.start_merge.value)
                        self.send_message("vanetza/in/denm", denm_message)

                    # Get the coordinate in the new route on wich we want to merge into
                    self.new_space = self.navigation.get_merge_location(self.adj_route)
                    # Send a new DENM message to the other cars with the merge point we want to go into
                    denm_message = self.generate_denm(self.new_space, CauseCode.merge_event.value, SubCauseCode.merge_location.value)
                    self.send_message("vanetza/in/denm", denm_message)

                    # Check if car has space for merging
                    has_space, cars_inside = self.has_space(self.adj_route)
                    if has_space:
                        self.state = "Merging"
                        print("OBU can merge")
                        # If it has, merge
                        self.merge()
                        self.lane_ending = False
                        started_merge = False
                        self.involved = False
                    # Slow down or any other mechanism and then merge
                    else:
                        print("OBU[{n}] CAN'T merge".format(n=self.id))
                        # If there's more than 3 cars inside where we want to merge, we just decelerate
                        if len(cars_inside) < 3:
                            car_behind = False
                            car_ahead = False
                            for car in cars_inside:
                                if self.other_cars[car]['position'] == 'behind':
                                    car_behind = True
                                    cb = car
                                if self.other_cars[car]['position'] == 'ahead':
                                    ch = car
                                    car_ahead = True
                            # If there's a car behind and a car ahead, meaning, between two vehicles
                            if car_behind and car_ahead:
                                if (self.speed + 5 <= self.other_cars[ch]['speed']):
                                    self.accelerate()
                            # If there's only one car behind
                            elif car_behind and not car_ahead:
                                print(bg.magenta + "OBU[{n}] is behind".format(n=cb) + bg.rs)
                                self.accelerate()
                            # If there's no car behind us, only ahead,
                            # we decrease speed and enter behind them
                            elif not car_behind:
                                print(bg.yellow + "OBU[{n}] is ahead".format(n=ch) + bg.rs)
                                self.decelerate()
                            # Else, we mantain velocity
                        else:
                            self.decelerate()

            if self.helping_merge:
                print("OBU[{n}] checking if he can help".format(n=self.id))
                # Go to the adjacent route
                self.state = "Evaluating Merge"
                # If the merge has started, we send a message indicating so
                self.adj_route = self.navigation.get_adj_route()
                if self.adj_route is not None:
                    self.new_space = self.navigation.get_merge_location(self.adj_route)
                    # Check if car has space for merging
                    has_space, cars_inside = self.has_space(self.adj_route)
                    if has_space:
                        self.state = "Merging"
                        print("OBU[{n}] can merge".format(n=self.id))
                        denm_message = self.generate_denm(self.coords, CauseCode.merge_event.value, SubCauseCode.helped_merge.value)
                        self.send_message("vanetza/in/denm", denm_message)
                        # If it has, merge
                        self.merge()
                        self.helping_merge = False
                    else:
                        print("OBU[{n}] can't help".format(n=self.id))
                        self.helping_merge = False
                else:
                    print("OBU[{n}] can't help".format(n=self.id))
                    self.helping_merge = False

            # Tick rate for the OBU
            time.sleep(0.5)
            if end:
                self.finished = True

        client.loop_stop()
        client.disconnect()
        print(bg.red + "OBU[{n}] ended it's run".format(n=self.id) + bg.rs)

    def __repr__(self) -> str:
        return (
            "Name: "
            + self.name
            + " OBU ID["
            + str(self.id)
            + "] | Address: "
            + self.address
            + " | State: "
            + self.state
            + "\n"
        )

    def generate_cam(self):
        cam_message = CAM(
            True,
            10.0,
            0,
            0,
            False,
            True,
            True,
            0,
            "FORWARD",
            False,
            True,
            0,
            0,
            self.coords[0],
            self.length,
            self.coords[1],
            0,
            0,
            0,
            SpecialVehicle(PublicTransportContainer(False)),
            self.speed,
            0,
            True,
            self.id,
            15,
            self.width,
            0,
        )
        return cam_message.to_dict()

    def generate_denm(self, coordinates, cause_code, sub_cause_code):
        denm_message = DENM(
            Management(
                ActionID(self.id, 0),
                100.0,
                100.0,
                EventPosition(
                    coordinates[0],
                    coordinates[1],
                    PositionConfidenceEllipse(0, 0, 0),
                    Altitude(0, 1),
                ),
                0,
                15,
            ),
            Situation(7, EventType(cause_code, sub_cause_code)),
        )
        return denm_message.to_dict()

    def update_road_state(self, si, lat, lon, speed):
        # If we've already created a dict for this OBU, we update, else, we create
        if self.other_cars.get(si) is not None:
            self.other_cars[si]['lat'] = lat
            self.other_cars[si]['lon'] = lon
            self.other_cars[si]['speed'] = speed
            if self.navigation.is_behind((lat, lon), self.coords):
                # print("OBU[{n}] is behind OBU[{n2}]".format(n=si, n2=self.id))
                self.other_cars[si]['position'] = "behind"
            else:
                # print("OBU[{n}] is ahead OBU[{n2}]".format(n=si, n2=self.id))
                self.other_cars[si]['position'] = "ahead"
        else:
            # When we create a state for a car, by default we set that he is involved on the merge
            self.other_cars[si] = {'lat': lat, 'lon': lon, 'speed': speed, 'position': 'behind', 'involved': 'yes'}
