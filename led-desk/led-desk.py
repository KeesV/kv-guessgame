import paho.mqtt.client as mqtt
import uuid
import os
import time
import RPi.GPIO as GPIO

client_name = "led-desk-" + str(uuid.uuid4())
host_name = os.getenv("MQTT_HOST")
base_topic = os.getenv("MQTT_BASE_TOPIC")

# RGB LED pin configuration
pinRed = 17
pinGreen = 27
pinBlue = 22

# GPIO setup.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Zet de GPIO pinnen als uitgang.
GPIO.setup(pinRed, GPIO.OUT)
GPIO.setup(pinGreen, GPIO.OUT)
GPIO.setup(pinBlue, GPIO.OUT)

# Gebruik PWM op de pinnen.
red = GPIO.PWM(pinRed, 1000)
green = GPIO.PWM(pinGreen, 1000)
blue = GPIO.PWM(pinBlue, 1000)
red.start(0)
green.start(0)
blue.start(0)

sleepStep = 0.05

mqttClient = mqtt.Client(client_name)


def blink_start():
    print("Blinking start")
    red.ChangeDutyCycle(0)
    blue.ChangeDutyCycle(0)
    for dc in range(0, 101, 5):  # Loop 0 to 100 stepping dc by 5 each loop
        green.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)
    for i in range(0, 3, 1):
        for dc in range(95, 75, -5):  # Loop 95 to 5 stepping dc down by 5 each loop
            green.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
        for dc in range(75, 101, 5):  # Loop 95 to 5 stepping dc down by 5 each loop
            green.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)


def blink_stop():
    print("Blinking stop")
    green.ChangeDutyCycle(0)
    blue.ChangeDutyCycle(0)
    for dc in range(0, 101, 5):  # Loop 0 to 100 stepping dc by 5 each loop
        red.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)
    for i in range(0, 3, 1):
        for dc in range(95, 75, -5):  # Loop 95 to 5 stepping dc down by 5 each loop
            red.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
        for dc in range(75, 101, 5):  # Loop 95 to 5 stepping dc down by 5 each loop
            red.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
    for dc in range(101, 0, -1):  # Loop 0 to 100 stepping dc by 5 each loop
        red.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)


def blink_wait():
    print("Blinking wait")
    red.ChangeDutyCycle(0)
    green.ChangeDutyCycle(0)
    for dc in range(0, 101, 5):  # Loop 0 to 100 stepping dc by 5 each loop
        blue.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)
    blink_wait_shimmer()


def blink_wait_shimmer():
    print("Blinking wait shimmer")
    for i in range(0, 3, 1):
        for dc in range(95, 75, -5):  # Loop 95 to 5 stepping dc down by 5 each loop
            blue.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
        for dc in range(75, 101, 5):  # Loop 95 to 5 stepping dc down by 5 each loop
            blue.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)


def blink_correct():
    print("Blinking correct")
    red.ChangeDutyCycle(0)
    blue.ChangeDutyCycle(0)
    for dc in range(0, 56, 5):  # Loop 0 to 100 stepping dc by 5 each loop
        green.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)
    for i in range(0, 3, 1):
        for dc in range(56, 30, -5):  # Loop 95 to 5 stepping dc down by 5 each loop
            green.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
        for dc in range(30, 56, 5):  # Loop 95 to 5 stepping dc down by 5 each loop
            green.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
    for dc in range(56, 0, -5):  # Loop 0 to 100 stepping dc by 5 each loop
        green.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)


def blink_incorrect():
    print("Blinking incorrect")
    green.ChangeDutyCycle(0)
    blue.ChangeDutyCycle(0)
    for dc in range(0, 56, 5):  # Loop 0 to 100 stepping dc by 5 each loop
        red.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)
    for i in range(0, 3, 1):
        for dc in range(56, 30, -5):  # Loop 95 to 5 stepping dc down by 5 each loop
            red.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
        for dc in range(30, 56, 5):  # Loop 95 to 5 stepping dc down by 5 each loop
            red.ChangeDutyCycle(dc)
            time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
            print(dc)
    for dc in range(56, 0, -5):  # Loop 0 to 100 stepping dc by 5 each loop
        red.ChangeDutyCycle(dc)
        time.sleep(sleepStep)  # wait .05 seconds at current LED brightness
        print(dc)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT at '" + host_name + "' as '" + client_name + "'.")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to '" + base_topic + "/command'.")


def on_message(client, userdata, message):
    content = str(message.payload.decode("utf-8"))
    print("message received ", content)
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if content == "START":
        blink_start()
    elif content == "STOP":
        blink_stop()
    elif content == "WAIT":
        blink_wait
    elif content == "WAIT_SHIMMER":
        blink_wait_shimmer()
    elif content == "CORRECT":
        blink_correct()
    elif content == "INCORRECT":
        blink_incorrect()


mqttClient.on_connect
mqttClient.on_subscribe
mqttClient.on_message = on_message

mqttClient.connect(host_name)
mqttClient.subscribe(base_topic + "/command")

try:
    mqttClient.loop_forever()
finally:
    GPIO.cleanup()
