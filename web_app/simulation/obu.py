from platform import python_compiler
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import random
from simulation.messages.cam import CAM, PublicTransportContainer, SpecialVehicle
from simulation.messages.denm import DENM


class OBU:
    def __init__(self, name, id, address, height, width, route, speed):
        self.name = name
        self.id = id
        self.address = address
        self.route = route
        self.height = height
        self.width = width
        self.coords = route.get_position()
        self.state = "Gathering Info"
        self.speed = speed
        print("Speed: " + str(self.speed))
        self.finished = False

    def set_coords(self, coords):
        self.coords = coords

    def set_state(self, state):
        self.state = state

    def set_speed(self, speed):
        self.speed = speed

    def set_route(self, route):
        self.route = route

    def set_finished(self, finished):
        self.finished = finished

    def accelerate(self):
        pass

    def decelerate(self):
        pass

    def send_message(self, message):
        publish.single(
            "vanetza/in/cam", json.dumps(message), hostname=self.address
        )
    def decide_next_move(self):
        #print("OBU " + str(self.id) + " recieved message")
        #msg = json.loads(message.payload)
        #print(msg['latitude'])
        pass
    

    def handle_message(self,client,userdata,message):
        msg_type = message.topic

        if msg_type == "vanetza/out/cam":
            print("OBU " + str(self.id) + " recieved CAM message")
            print(message.payload)
        if msg_type == "vanetza/out/denm":
            print("OBU " + str(self.id) + " recieved DENM message")
            print(message.payload)

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

    def start(self):
        client = mqtt.Client(self.name)
        client.connect(self.address)
        client.on_message = self.handle_message
        client.loop_start()
        client.subscribe(topic=[("vanetza/out/denm",0),("vanetza/out/cam",0)])

        while not self.finished:
            self.set_coords(self.route.next_coord(speed=0))
            cam_message = self.generate_cam()
            self.send_message(cam_message)
            time.sleep(0.5)

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
