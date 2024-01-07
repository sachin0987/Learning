import requests
import base64
import json

# NSO credentials and details
NSO_USERNAME = 'your_username'
NSO_PASSWORD = 'your_password'
NSO_URL = 'https://your_nso_server_ip:your_nso_port/restconf/data/tailf-ncs:devices'

def check_sync_status(device_hostname):
    auth = base64.b64encode(f"{NSO_USERNAME}:{NSO_PASSWORD}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }

    device_url = f"{NSO_URL}/device={device_hostname}"
    try:
        response = requests.get(device_url, headers=headers, verify=False)
        if response.status_code == 200:
            device = response.json().get('tailf-ncs:device', {})
            device_name = device.get('name', '')
            sync_status = device.get('sync-status', '')

            if device_name:
                print(f"Device {device_name} is {'in sync' if sync_status == 'in-sync' else 'out of sync'} - Sync Status: {sync_status}")
                if sync_status != 'in-sync':
                    sync_device(device_name, headers)
            else:
                print(f"Device with hostname {device_hostname} not found.")
        else:
            print(f"Failed to fetch device {device_hostname}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")

def sync_device(device_name, headers):
    sync_url = f"{NSO_URL}/device={device_name}/sync-from"
    try:
        response = requests.post(sync_url, headers=headers, verify=False)
        if response.status_code == 200:
            print(f"Sync initiated for device {device_name}")
        else:
            print(f"Failed to sync device {device_name}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")

if __name__ == "__main__":
    device_hostname = input("Enter the device hostname: ")
    check_sync_status(device_hostname)
