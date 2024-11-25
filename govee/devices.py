import requests

# Govee API key
GOVEE_API_KEY = '929f506f-f061-4b3d-9cc1-117730797b7c'

# Function to retrieve devices
def get_govee_devices():
    headers = {
        'Govee-API-Key': GOVEE_API_KEY
    }
    url = 'https://developer-api.govee.com/v1/devices'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        devices = response.json()
        print("Devices:")
        print(devices)
    else:
        print(f"Failed to retrieve devices. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

get_govee_devices()
