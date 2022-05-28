import paho.mqtt.client as mqttClient
import time
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
    while True:
        time.sleep(1)

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
            1,
            15,
            30,
            0,
        )

        msg = '{\
                "accEngaged":true,\
                "acceleration":0,\
                "altitude":800001,\
                "altitudeConf":15,\
                "brakePedal":true,\
                "collisionWarning":true,\
                "cruiseControl":true,\
                "curvature":1023,\
                "driveDirection":"FORWARD",\
                "emergencyBrake":true,\
                "gasPedal":false,\
                "heading":3601,\
                "headingConf":127,\
                "latitude":400000000,\
                "length":100,\
                "longitude":-80000000,\
                "semiMajorConf":4095,\
                "semiMajorOrient":3601,\
                "semiMinorConf":4095,\
                "specialVehicle":{\
                    "publicTransportContainer":{\
                        "embarkationStatus":false\
                    }\
                },\
                "speed":16383,\
                "speedConf":127,\
                "speedLimiter":true,\
                "stationID":1,\
                "stationType":15,\
                "width":30,\
                "yawRate":10\
            }'

        result = client.publish(publish_topic, msg)

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
    publish(client)
    # subscribe(client)
    client.loop_forever()


# ------------------------------------------ Main Function ----------------------------------------
if __name__ == "__main__":
    run()
