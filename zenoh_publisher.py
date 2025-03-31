import time
import json
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
import zenoh

# Create the I2C bus and ADC object
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P1)  # Use channel 1 for potentiometer input

# Zenoh setup
z_config = zenoh.Config()
z_session = zenoh.open(z_config)

# Zenoh Key/Topic
KEY = 'vehicle/speed'

def publisher():
    while True:
        # Read potentiometer value
        pot_value = chan.value
        speed = int((pot_value / 26350) * 100)  # Scale 0-100

        # Get current timestamp
        timestamp = datetime.utcnow().isoformat()

        # Create message payload
        message = {
            'speed': speed,
            'timestamp': timestamp
        }

        # Publish message via Zenoh
        z_session.put(KEY, json.dumps(message))
        print(f"Published speed: {speed} with timestamp {timestamp}")

        time.sleep(1)

    z_session.close()
    print("Publisher finished.")

if __name__ == "__main__":
    publisher()

