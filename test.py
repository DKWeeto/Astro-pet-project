import base64
from os import environ as ENV
from dotenv import load_dotenv
import requests
load_dotenv()
userpass = f"{ENV['APP_ID']}:{ENV['APP_SECRET']}"
authString = base64.b64encode(userpass.encode()).decode()
response = requests.get(
    "https://api.astronomyapi.com/api/v2/bodies/positions?longitude=-84.39733&latitude=33.775867&elevation=1&from_date=2024-05-16&to_date=2024-05-16&time=15%3A03%3A58", headers={"Authorization": f"Basic {authString}"})
print(response.json())