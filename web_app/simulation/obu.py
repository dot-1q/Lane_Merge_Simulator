import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
from simulation.messages.cam import CAM, PublicTransportContainer, SpecialVehicle
from simulation.messages.denm import DENM


class OBU:
    def __init__(self, name, id, address, height, width, route):
        self.name = name
        self.id = id
        self.address = address
        self.route = route
        self.height = height
        self.width = width
        self.coords = route.get_position()
        self.state = "Gathering Info"
        self.speed = 100
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

    def decide_next_move(self, client, userdata, message):
        print("OBU " + str(self.id) + " recieved message")
        msg = json.loads(message.payload)
        #print(msg['latitude'])

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
        denm_client = mqtt.Client(self.name)
        denm_client.connect(self.address)
        denm_client.on_message = self.decide_next_move
        denm_client.loop_start()
        denm_client.subscribe("vanetza/out/denm")

        cam_client = mqtt.Client(self.name)
        cam_client.connect(self.address)
        cam_client.on_message = self.decide_next_move
        cam_client.loop_start()
        cam_client.subscribe("vanetza/out/cam")
        while not self.finished:
            self.set_coords(self.route.next_coord(speed=0))
            cam_message = self.generate_cam()
            self.send_message(cam_message)
            time.sleep(2)

        denm_client.loop_stop()
        denm_client.disconnect()

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
