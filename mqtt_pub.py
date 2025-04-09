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

# MQTT Broker Configuration
BROKER = '127.0.0.1'
PORT = 1883
PUBLISH_TOPIC = 'vehicle/speed'

# Set up I2C and ADC (ADS1115)
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P1)

# SPI setup for MCP3008 (if needed)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def publisher():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        while True:
            pot_value = chan.value
            speed = int((pot_value / 26350) * 100)  # Normalize to 0–100

            timestamp = datetime.utcnow().isoformat()

            payload = {
                "speed": speed,
                "timestamp": timestamp
            }

            client.publish(PUBLISH_TOPIC, json.dumps(payload))
            print(f"Published: {payload}")
            sleep(1)

    except KeyboardInterrupt:
        print("Exiting publisher...")

    finally:
        client.loop_stop()
        client.disconnect()
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    publisher()

