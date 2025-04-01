from kuksa_client.grpc import VSSClient
from datetime import datetime

# KUKSA DataBroker details
KUKSA_HOST = "127.0.0.1"
KUKSA_PORT = 55555

try:
    with VSSClient(KUKSA_HOST, KUKSA_PORT) as client:
        print("Subscribed to Vehicle.Speed updates...\n")

        # Subscribe to speed values
        for updates in client.subscribe_current_values(['Vehicle.Speed']):
            if 'Vehicle.Speed' in updates:
                speed = updates['Vehicle.Speed'].value
                timestamp = datetime.utcnow().isoformat()
                print(f"[{timestamp}] Received updated speed: {speed}")
            else:
                print(f"[{datetime.utcnow().isoformat()}] No update received for Vehicle.Speed.")

except Exception as e:
    print(f"Error in subscriber: {e}")
