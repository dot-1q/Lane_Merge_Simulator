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

    def send_message(self, topic, message):
        publish.single(topic, json.dumps(message), hostname=self.address)

    def decide_next_move(self):
        # print("OBU " + str(self.id) + " recieved message")
        # msg = json.loads(message.payload)
        # print(msg['latitude'])
        pass

    def handle_message(self, client, userdata, message):
        msg_type = message.topic

        if msg_type == "vanetza/out/cam":
            print("OBU " + str(self.id) + " recieved CAM message")
            # print(message.payload)
        if msg_type == "vanetza/out/denm":
            print("OBU " + str(self.id) + " recieved DENM message")
            # print(message.payload)

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
            # update cars position
            self.coords = self.navigation.get_coords(self.speed)
            cam_message = self.generate_cam()
            self.send_message("vanetza/in/cam",cam_message)
            time.sleep(1)
            if self.navigation.get_position() > 110:
                if self.name == "car_merge":
                    self.navigation.set_route("lane_1")

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
