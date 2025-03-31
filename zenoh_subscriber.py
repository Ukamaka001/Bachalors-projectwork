import time
import json
import zenoh

# Zenoh setup
z_config = zenoh.Config()
z_session = zenoh.open(z_config)

# Zenoh Key/Topic
KEY = 'vehicle/speed'

def callback(sample):
    try:
        # Convert the payload to bytes and decode it as UTF-8
        payload = bytes(sample.payload).decode("utf-8")
        # Parse the JSON message
        message = json.loads(payload)
        print(f"Received speed: {message['speed']} with timestamp {message['timestamp']}")
    except Exception as e:
        print(f"Error processing message: {e}")

def subscriber():
    # Use declare_subscriber to subscribe to the topic
    z_subscriber = z_session.declare_subscriber(KEY, callback)
    print(f"Subscribed to {KEY}, waiting for messages...")

    try:
        while True:
            time.sleep(1)  # Keep the subscriber running
    except KeyboardInterrupt:
        print("Subscriber exiting...")
    finally:
        z_session.undeclare_subscriber(z_subscriber)
        z_session.close()

if __name__ == "__main__":
    subscriber()

