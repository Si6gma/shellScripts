import requests

# Replace with your Govee API key
API_KEY = '929f506f-f061-4b3d-9cc1-117730797b7c'

# Base URL for Govee API control endpoint
base_url = 'https://developer-api.govee.com/v1/devices/control'

# API headers including your API key
headers = {
    'Govee-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Function to control the device and set a dynamic scene
def set_dynamic_scene(device_id, model, scene_name):
    payload = {
        "device": device_id,
        "model": model,
        "cmd": {
            "name": "scene",
            "value": scene_name
        }
    }

    # Send POST request to Govee API
    response = requests.put(base_url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Dynamic scene '{scene_name}' set successfully for device {device_id}")
    else:
        print(f"Failed to set dynamic scene '{scene_name}' for device {device_id}, Error: {response.status_code}, Response: {response.text}")

# Example: Setting a dynamic scene on all devices
devices = [
    {"device_id": "0F:3F:D0:C9:07:30:0D:18", "model": "H6008"},
    {"device_id": "63:53:D0:C9:07:3B:30:B2", "model": "H6008"},
    {"device_id": "55:8D:D0:C9:07:39:1A:D0", "model": "H6008"}
]

# Replace with a dynamic scene from your app (e.g., "Dusk", "Sunset Glow", "Fire")
scene_name = "Dusk"

for device in devices:
    set_dynamic_scene(device['device_id'], device['model'], scene_name)