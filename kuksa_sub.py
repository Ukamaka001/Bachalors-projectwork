from kuksa_client.grpc import VSSClient

# KUKSA.val setup
KUKSA_HOST = "127.0.0.1"
KUKSA_PORT = 55555

def on_speed_update(value):
    print(f"Speed updated: {value}")

try:
    with VSSClient(KUKSA_HOST, KUKSA_PORT) as kuksa_client:
        print("Subscribing to Vehicle.Speed...")
        kuksa_client.subscribe("Vehicle.Speed", on_speed_update)

        # Keep running
        input("Press Enter to exit...\n")

except Exception as e:
    print(f"Error: {e}")
