# publisher/publisher.py

import spidev  # For MCP3008 ADC
import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
from datetime import datetime
import json

import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0 (for potentiometer)
chan = AnalogIn(ads, ADS.P1)

# MQTT Broker Configuration
BROKER = "8f7be027a187404b865072adb33d1672.s1.eu.hivemq.cloud"
PORT = 8883
PUBLISH_TOPIC = 'vehicle/speed'
USER = 'publisher'
PASS = 'Aku-12345'

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {rc}")
    # Subscribe to a topic after connecting
    client.subscribe("#")

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} -> {msg.payload.decode()}")

def publisher():
    client = mqtt.Client()
    client.tls_set()   #!!!!!!!!!!!!!
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(USER, PASS)
    client.connect(BROKER, PORT, 60)
    

    
    while True:
        # Read potentiometer value
        pot_value = chan.value
        speed = int((pot_value / 26350) * 100)  # Scale 0-100

        # Get the current timestamp
        timestamp = datetime.utcnow().isoformat()

        # Create message payload
        message = {
            'speed': speed,
            'timestamp': timestamp
        }

        # Publish the message to the MQTT broker
        client.publish(PUBLISH_TOPIC, json.dumps(message))
        print(f"Published speed: {speed} with timestamp {timestamp}")
        sleep(1)

    client.disconnect()
    print("Finished publishing.")

if __name__ == "__main__":
    publisher()
