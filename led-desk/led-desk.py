import paho.mqtt.client as mqtt
import uuid
import os

client_name = "led-desk-" + str(uuid.uuid4())
host_name = os.getenv("MQTT_HOST")
base_topic = os.getenv("MQTT_BASE_TOPIC")

mqttClient = mqtt.Client(client_name)

mqttClient.connect(host_name)
mqttClient.subscribe("led-desk-downstairs/command")


def on_message(client, userdata, message):
    content = str(message.payload.decode("utf-8"))
    print("message received ", content)
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


mqttClient.on_message = on_message

mqttClient.loop_forever()