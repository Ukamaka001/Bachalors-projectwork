import spidev  # For MCP3008 ADC
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from kuksa_client.grpc import Datapoint
from kuksa_client.grpc import DataEntry
from kuksa_client.grpc import DataType
from kuksa_client.grpc import EntryUpdate
from kuksa_client.grpc import Field
from kuksa_client.grpc import Metadata
from kuksa_client.grpc import VSSClient
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P1)

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# KUKSA.val setup
KUKSA_HOST = "127.0.0.1"
KUKSA_PORT = 55555

def publish_to_kuksa(val_client, speed, timestamp):
    try:
        #val_client.set_current_values({'Vehicle.Speed': Datapoint(new_speed)})
        val_client.set_current_values({'Vehicle.Speed': Datapoint(speed)})
        print(f"Published to KUKSA.val: Speed={speed}, Timestamp={timestamp}")
    except Exception as e:
        print(f"Error publishing to KUKSA.val: {e}")

try:
    with VSSClient(KUKSA_HOST, KUKSA_PORT) as kuksa_client:
        while True:
            # Read potentiometer value
            pot_value = chan.value
            speed = int((pot_value / 26350) * 100)  # Scale 0-100
            timestamp = datetime.utcnow().isoformat()

            # Publish to KUKSA
            publish_to_kuksa(kuksa_client, speed, timestamp)

            sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
    spi.close()
