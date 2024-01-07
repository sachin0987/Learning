import requests
import json

# Define your Crosswork API endpoint and credentials
crosswork_api = "https://your-crosswork-api-endpoint"
username = "your_username"
password = "your_password"

# Function to get the ticket
def get_ticket():
    ticket_url = f"{crosswork_api}/v1/tickets"
    response = requests.post(ticket_url, auth=(username, password))
    if response.status_code == 201:
        return response.json().get('serviceTicket')
    else:
        print("Failed to get the ticket.")
        return None

# Function to get the authentication token
def get_auth_token(ticket):
    auth_url = f"{crosswork_api}/v1/auth/token"
    headers = {
        "X-Auth-Token": ticket
    }
    response = requests.post(auth_url, headers=headers)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print("Failed to get the authentication token.")
        return None

# Function to register a device
def register_device(device_info, token):
    register_url = f"{crosswork_api}/v1/devices"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(register_url, headers=headers, json=device_info)
    if response.status_code == 200:
        print("Device registered successfully.")
    else:
        print("Device registration failed.")

# Device information (example, modify as per your device details)
device_info = {
    "name": "Device_Name",
    "type": "Device_Type",
    "ipAddress": "Device_IP",
    # Add more device information as required
}

# Main execution
if __name__ == "__main__":
    ticket = get_ticket()
    if ticket:
        token = get_auth_token(ticket)
        if token:
            register_device(device_info, token)
