from kuksa_client.grpc import VSSClient
from kuksa_client.grpc import Datapoint
import time
from datetime import datetime

# Publisher
with VSSClient('127.0.0.1', 55555) as client:
    for speed in range(0, 100):
        # Get the current timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # Send the speed and timestamp
        client.set_current_values({
            'Vehicle.Speed': Datapoint(speed),
            'Vehicle.CurrentLocation.Timestamp': Datapoint(timestamp),
        })
        
        print(f"Feeding Vehicle.Speed to {speed} with timestamp {timestamp}")
        time.sleep(1)

print("Finished.")
