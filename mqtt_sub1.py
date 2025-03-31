# subscriber/subscriber.py

import paho.mqtt.client as mqtt
from datetime import datetime
import json

# MQTT Broker Configuration
BROKER = '127.0.0.1'
PORT = 1883
SUBSCRIBE_TOPIC = 'vehicle/speed'

def on_message(client, userdata, msg):
    received_time = datetime.utcnow()

    # Parse the message
    payload = json.loads(msg.payload.decode())
    speed = payload['speed']
    sent_timestamp = datetime.fromisoformat(payload['timestamp'])

    # Calculate delay
    delay = (received_time - sent_timestamp).total_seconds()
    print(f"Received speed: {speed}, sent at {sent_timestamp}, received at {received_time}, delay: {delay:.3f} seconds")

def subscriber():
    client = mqtt.Client()
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.subscribe(SUBSCRIBE_TOPIC)

    print("Subscriber is running...")
    client.loop_forever()

if __name__ == "__main__":
    subscriber()
