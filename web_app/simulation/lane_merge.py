import paho.mqtt.client as mqttClient
import time
import json
from messages.cam import CAM, SpecialVehicle, PublicTransportContainer

# Global variables
id = "Lane Merge"
rsu_ip = "192.168.98.254"
subscribe_topic = "vanetza/out/cam"
publish_topic = "vanetza/in/cam"

# Method to connect to MQTT -> returns an client of the mqttClient type
def connect_mqtt() -> mqttClient:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqttClient.Client(id)
    client.on_connect = on_connect
    client.connect(rsu_ip)
    return client


# Publish a message to the topic -> it receives an client of the mqttClient type
def publish(client):
    # TODO -> in the toString method of CAM class the boolean values (True and False)
    # should be changes to lower case letters, like "true" and "false"
    # otherwise vanetza will no be capable to understand the syntax
    msg = CAM(
        True,
        0,
        800001,
        15,
        True,
        True,
        True,
        1023,
        "FORWARD",
        True,
        False,
        3601,
        127,
        400000000,
        100,
        -80000000,
        4095,
        3601,
        4095,
        SpecialVehicle(PublicTransportContainer(False)),
        16383,
        127,
        True,
        2,
        5,
        30,
        100
    )

    result = client.publish(publish_topic, json.dumps(msg.to_dict()))

    # result: [0, 1]
    status = result[0]

    if status == 0:
        print(f"Send msg to topic '{publish_topic}'")
    else:
        print(f"Failed to send message to topic '{publish_topic}'")


# Subscribes the topic "vanetza/out/cam" -> it receives an client of the mqttClient type
def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}`")

    client.subscribe(subscribe_topic)
    client.on_message = on_message


# To run the main methods of the mqttClient
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    # subscribe(client)
    client.disconnect()
    client.loop_stop()

# ------------------------------------------ Main Function ----------------------------------------
if __name__ == "__main__":
    run()
