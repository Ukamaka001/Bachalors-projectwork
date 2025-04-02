import time
import json
import zenoh

# Create Zenoh config object
z_config = zenoh.Config()

# Use the correct way to set up connection configuration
z_config.insert_json5("connect/endpoints", '["tcp/172.31.12.43:7447"]')  # Corrected path

# Open a Zenoh session
z_session = zenoh.open(z_config)

# Zenoh Key/Topic
KEY = "vehicle/speed"

def callback(sample):
    try:
        # Convert the payload to bytes and decode as UTF-8
        payload = bytes(sample.payload).decode("utf-8")
        # Parse the JSON message
        message = json.loads(payload)
        print(f"Received speed: {message['speed']} with timestamp {message['timestamp']}")
    except Exception as e:
        print(f"Error processing message: {e}")

def subscriber():
    # Declare subscriber to the topic
    z_subscriber = z_session.declare_subscriber(KEY, callback)
    print(f"Subscribed to {KEY}, waiting for messages...")

    try:
        while True:
            time.sleep(1)  # Keep the subscriber running
    except KeyboardInterrupt:
        print("Subscriber exiting...")
    finally:
        z_session.close()

if __name__ == "__main__":
    subscriber()
