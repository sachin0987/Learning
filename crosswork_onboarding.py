import requests

url = "https://10.10.20.42:30603/SSO/v1/tickets?username=admin&password=Adm!n123!"

payload = ""
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'text/plain',
  'Cache-Control': 'no-cache'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)