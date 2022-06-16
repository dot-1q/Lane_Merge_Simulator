import time
import json
import os
import paho.mqtt.publish as publish
from simulation.messages.denm import *


class RSU:
    def __init__(self, name, id, address, width, height, coords):
        self.name = name
        self.id = id
        self.address = address
        self.width = width
        self.height = height
        self.coords = coords
        self.finished = False

    def set_coords(self, coords):
        self.coords = coords

    def set_finished(self, finished):
        self.finished = finished

    def send_message(self, message):
        print("Sending Intersection coordinates")
        publish.single("vanetza/in/denm", json.dumps(message), hostname=self.address)

    def start(self):
        print("RSU started")
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'coordinates', 'intersection.csv')
        with open(filename) as f:
            inter_coords = [(float(line[0]), float(line[1])) for line in [lines.split(',') for lines in f][1:]]

        while not self.finished:
            denm_message = DENM(
                Management(
                    ActionID(179858, 0),
                    100.0,
                    100.0,
                    EventPosition(
                        inter_coords[0][0],
                        inter_coords[0][1],
                        PositionConfidenceEllipse(0, 0, 0),
                        Altitude(0, 1),
                    ),
                    0,
                    15,
                ),
                Situation(7, EventType(CauseCode.intersection.value, 0)),
            )

            self.send_message(denm_message.to_dict())
            time.sleep(1)
