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
        self.other_cars = {}
        self.involved = True
        self.new_space = None
        self.evaluated_inter = False
        self.lane_ending = False

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
        pass

    def decelerate(self):
        pass

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
        # TODO : needs to be cleaner, since it's still hardcoded
        space_for_merge = self.navigation.space_between(new_route, self.length)
        car_coords = (self.other_cars[2]["lat"], self.other_cars[2]["lon"])

        # Check if the car is in the space we want to be in
        if self.navigation.check_in_between(space_for_merge, car_coords):
            print(bg.red + "OBU[2] is in the space we want to be in" + bg.rs)
            return False
        else:
            print(bg.blue + "OBU[2] is NOT the space we want to be in" + bg.rs)
            return True

    def merge(self):
        self.navigation.set_route("lane_1")
        # Set the new position in the new route
        # Still hardcoded, has to be cleaned up
        self.navigation.set_position(self.navigation.position + 5)

    def handle_message(self, client, userdata, message):
        msg_type = message.topic
        message = json.loads(message.payload)

        if msg_type == "vanetza/out/cam":
            cam_message = CAM.from_dict(message)
            si = cam_message.station_id
            speed = cam_message.speed
            lat = cam_message.latitude
            lon = cam_message.longitude
            # Update the road description upon recieving a cam
            self.other_cars[si] = {"lat": lat, "lon": lon, "speed": speed}
            pass

        if msg_type == "vanetza/out/denm":
            station_id = message["fields"]["denm"]["management"]["actionID"]["originatingStationID"]
            cause_code = message["fields"]["denm"]["situation"]["eventType"]["causeCode"]
            sub_cause_code = message["fields"]["denm"]["situation"]["eventType"]["subCauseCode"]
            lat = message["fields"]["denm"]["management"]["eventPosition"]["latitude"]
            lon = message["fields"]["denm"]["management"]["eventPosition"]["longitude"]

            # Check from cause code and sub cause code what type of situation it is
            if cause_code == 31 and self.involved:
                if sub_cause_code == 31:
                    print("OBU[{n}] Evaluating Merge Request from OBU[{n2}]".format(n=self.id, n2=station_id))

                    # Check if this car is ahead or behind the merge location
                    if self.navigation.is_behind((lat, lon), self.coords):
                        print(bg.red + "OBU[{n}] Merge pont is behind".format(n=self.id) + bg.rs)
                        denm_message = self.generate_denm(self.coords, CauseCode.merge_event.value, SubCauseCode.not_involved.value)
                        self.send_message("vanetza/in/denm", denm_message)
                        # This car is not involved in the merge
                        self.involved = False
                    else:
                        # Do Stuff
                        print(bg.blue + "OBU[{n}] Merge pont is ahead".format(n=self.id) + bg.rs)
                        self.involved = True

                if sub_cause_code == 32:
                    pass
                if sub_cause_code == 33:
                    pass
                if sub_cause_code == 34:
                    pass
                if sub_cause_code == 35:
                    print("OBU[{n}] | OBU[{n2}] stated that he is not involved".format(n=self.id, n2=station_id))
                    pass

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
        notified = False
        started_merge = False

        while not self.finished:
            # print("-------------- New TICK from OBU[" + str(self.id) + "]")
            # update cars position
            self.coords = self.navigation.get_coords(self.speed)
            cam_message = self.generate_cam()
            self.send_message("vanetza/in/cam", cam_message)

            # If this OBU's lane is ending, check it's distance to the intersection
            if self.lane_ending is True:
                distance = round(GD(self.coords, self.navigation.intersection).m, 3)
                print("Distance to the intersection = {d}".format(d=distance))

                # If distance to the intersectiion is less than 60m, we send a DENM about the merge request
                if distance < 40 or started_merge:
                    # TODO This is hard coded, and needs to be cleaned up
                    position = self.navigation.position
                    adj_route = self.navigation.get_route("lane_1")
                    self.new_space = adj_route.get_coords(position + 5)
                    # TODO This is hard coded, and needs to be cleaned up

                    # We only want to notify about the merge request once, then a decision making process is started
                    if notified is False:
                        notified = True
                        denm_message = self.generate_denm(self.new_space, CauseCode.merge_event.value, SubCauseCode.merge_request.value)
                        self.send_message("vanetza/in/denm", denm_message)
                        started_merge = True

                    # Check if car has space for merging
                    if self.has_space(self.navigation.get_route("lane_1")):
                        print("OBU can merge")
                        # If it has, merge
                        self.merge()
                    # Slow down or any other mechanism and then merge
                    else:
                        print("OBU CAN'T merge")
                        pass

            if self.involved:
                print(bg.magenta + "OBU[{n}] is involved in the merge".format(n=self.id) + bg.rs)
            else:
                print(bg.yellow + "OBU[{n}] NOT involved in the merge".format(n=self.id) + bg.rs)

            # Tick rate for the OBU
            time.sleep(1)

        client.loop_stop()
        client.disconnect()

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