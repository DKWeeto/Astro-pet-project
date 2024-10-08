"""Extract"""

import base64
from datetime import datetime, timedelta

from requests import get, post


def get_neos(config):
    """Get info about near earth objects this upcoming week"""
    response = get(
        f"https://api.nasa.gov/neo/rest/v1/feed?start_date={datetime.now().date()}&end_date=\
        {datetime.now().date() + timedelta(days=7)}&api_key={config['NASA_KEY']}",
        timeout=60)
    return response.json()["near_earth_objects"]


def get_pic_of_day(config):
    """Get today's pic of the day."""
    response = get(
        f"https://api.nasa.gov/planetary/apod?api_key={config['NASA_KEY']}",
        timeout=60).json()
    return response


def get_notifications(config):
    """Get space notifications"""
    return get(f"https://api.nasa.gov/DONKI/notifications?start_date=\
               {datetime.now().date()}&end_date={datetime.now().date() + timedelta(days=7)}\
               &type=all&api_key={config['NASA_KEY']}", timeout=60).json()


def get_body_positions(config, latitude, longitude):
    """Get all hourly celestial body positions for the upcoming night."""
    userpass = f"{config['APP_ID']}:{config['APP_SECRET']}"
    auth_string = base64.b64encode(userpass.encode()).decode()
    forecasts = []
    for hour in ['20', '21', '22', '23']:
        forecasts.append(get(f"https://api.astronomyapi.com/api/v2/bodies/positions?latitude={latitude}&longitude={longitude}&elevation=0&from_date={datetime.now().date()}&to_date={datetime.now().date()}&time={hour}:00:00",
                             headers={"Authorization": f"Basic {auth_string}"}, timeout=60).json())
    for hour in ['00', '01', '02', '03', '04']:
        forecasts.append(get(f"https://api.astronomyapi.com/api/v2/bodies/positions?latitude={latitude}&longitude={longitude}&elevation=0&from_date={datetime.now().date() + timedelta(days=1)}&to_date={datetime.now().date() + timedelta(days=1)}&time={hour}:00:00",
                             headers={"Authorization": f"Basic {auth_string}"}, timeout=60).json())
    return forecasts


def get_star_charts(config: dict, latitude: float, longitude: float,
                    constellation_code: str = "umi"):
    """Get all hourly star charts for the upcoming night"""
    userpass = f"{config['APP_ID']}:{config['APP_SECRET']}"
    auth_string = base64.b64encode(userpass.encode()).decode()
    red_chart = post("https://api.astronomyapi.com/api/v2/studio/star-chart",
                     f'{{"style":"red","observer":{{"latitude":{latitude},"longitude":\
                        {longitude},"date":"{datetime.now().date()}"}},"view":\
                            {{"type":"constellation","parameters":\
                            {{"constellation":"{constellation_code}"}},"zoom":6}}}}',
                     headers={"Authorization": f"Basic {auth_string}"}, timeout=300).json()
    default_chart = post("https://api.astronomyapi.com/api/v2/studio/star-chart",
                         f'{{"style":"default","observer":{{"latitude":{latitude},"longitude":\
                            {longitude},"date":"{datetime.now().date()}"}},"view":\
                                {{"type": "constellation", "parameters":\
                                {{"constellation": "{constellation_code}"}}, "zoom": 6}}}}',
                         headers={"Authorization": f"Basic {auth_string}"}, timeout=300).json()
    return red_chart, default_chart
