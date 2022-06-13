import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import random
from simulation.messages.cam import CAM, PublicTransportContainer, SpecialVehicle
from simulation.messages.denm import *


class OBU:
    def __init__(self, name, id, address, height, width, navigation, speed):
        self.name = name
        self.id = id
        self.address = address
        self.height = height
        self.width = width
        self.state = "Gathering Info"
        self.speed = speed
        self.finished = False
        self.navigation = navigation
        self.coords = self.navigation.get_coords(self.speed)

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

    def handle_message(self, client, userdata, message):
        msg_type = message.topic
        message = json.loads(message.payload)

        if msg_type == "vanetza/out/cam":
            print("OBU [" + str(self.id) + "] Recieved CAM with lat: " + str(message['latitude']) + " lon: " + str(message['longitude']))

        if msg_type == "vanetza/out/denm":
            print("OBU " + str(self.id) + " recieved DENM message")
            cause_code = message["fields"]["denm"]["situation"]["eventType"]["causeCode"]
            sub_cause_code = message["fields"]["denm"]["situation"]["eventType"]["subCauseCode"]

            # Check from cause code and sub cause code what type of situation it is
            if cause_code == 31:
                pass

            elif cause_code == 32:
                pass

            elif cause_code == 33:
                pass

            elif cause_code == 34:
                pass

            elif cause_code == 35:
                lat = message["fields"]["denm"]["management"]["eventPosition"]["latitude"]
                lon = message["fields"]["denm"]["management"]["eventPosition"]["longitude"]

                # it's an intersection denm
                print("Check if intersection point is in own route")
                if self.in_own_route((lat, lon)):
                    print("In my route | OBU {n}".format(n=self.id))
                else:
                    print("NOT in my route | OBU {n}".format(n=self.id))

        self.decide_next_move()

    def generate_cam(self):
        cam_message = CAM(
            True,
            10,
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
            self.height,
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

    def generate_denm(self, cause_code):
        denm_message = DENM(
            Management(
                ActionID(179858, 0),
                100.0,
                100.0,
                EventPosition(
                    self.coords[0],
                    self.coords[1],
                    PositionConfidenceEllipse(0, 0, 0),
                    Altitude(0, 1),
                ),
                0,
                15,
            ),
            Situation(7, EventType(cause_code, 0)),
        )
        return denm_message.to_dict()

    def start(self):
        client = mqtt.Client(self.name)
        client.connect(self.address)
        client.on_message = self.handle_message
        client.loop_start()
        client.subscribe(topic=[("vanetza/out/denm", 0), ("vanetza/out/cam", 0)])

        while not self.finished:
            print("-------------- New TICK from OBU[" + str(self.id) + "]")
            # update cars position
            self.coords = self.navigation.get_coords(self.speed)
            cam_message = self.generate_cam()
            self.send_message("vanetza/in/cam", cam_message)
            # Podes ignorar, é so para trocar de rota
            if self.navigation.get_position() > 110:
                if self.name == "car_merge":
                    self.navigation.set_route("lane_1")
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
