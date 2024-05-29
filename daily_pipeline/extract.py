from requests import get, post
from os import environ as ENV
from dotenv import load_dotenv
from datetime import datetime, timedelta
import base64


def get_neos(config):
    """Get info about near earth objects this upcoming week"""
    response = get(
        f"https://api.nasa.gov/neo/rest/v1/feed?start_date={datetime.now().date()}&end_date={datetime.now().date() + timedelta(days=7)}&api_key={config['NASA_KEY']}")
    return response.json()["near_earth_objects"]


def get_pic_of_day(config):
    """Get today's pic of the day."""
    return get(f"https://api.nasa.gov/planetary/apod?api_key={config['NASA_KEY']}").json()


def get_notifications(config):
    return get(f"https://api.nasa.gov/DONKI/notifications?start_date={datetime.now().date()}&end_date={datetime.now().date() + timedelta(days=7)}&type=all&api_key={config['NASA_KEY']}").json()


def get_body_positions(config, latitude, longitude):
    """Get all hourly celestial body positions for the upcoming night."""
    userpass = f"{config['APP_ID']}:{config['APP_SECRET']}"
    authString = base64.b64encode(userpass.encode()).decode()
    forecasts = []
    for hour in ['20', '21', '22', '23', '00', '01', '02', '03', '04']:
        forecasts.append(get(f"https://api.astronomyapi.com/api/v2/bodies/positions?latitude={latitude}&longitude={longitude}&elevation=0&from_date={datetime.now().date()}&to_date={datetime.now().date()}&time={hour}:00:00", headers={
                         "Authorization": f"Basic {authString}"}).json())
    return forecasts


def get_star_charts(config, latitude, longitude):
    """Get all hourly star charts for the upcoming night"""
    userpass = f"{config['APP_ID']}:{config['APP_SECRET']}"
    authString = base64.b64encode(userpass.encode()).decode()
    red_chart = post("https://api.astronomyapi.com/api/v2/studio/star-chart",
                     f'{{"style":"red","observer":{{"latitude":{latitude},"longitude":{longitude},"date":"{datetime.now().date()}"}},"view":{{"type":"constellation","parameters":{{"constellation":"umi"}},"zoom":6}}}}',
                     headers={"Authorization": f"Basic {authString}"}).json()
    default_chart = post("https://api.astronomyapi.com/api/v2/studio/star-chart",
                         f'{{"style":"default","observer":{{"latitude":{latitude},"longitude":{longitude},"date":"{datetime.now().date()}"}},"view":{{"type":"constellation","parameters":{{"constellation":"umi"}},"zoom":6}}}}',
                         headers={"Authorization": f"Basic {authString}"}).json()
    return red_chart, default_chart


if __name__ == "__main__":
    load_dotenv()
    print(get_neos(ENV))
    print(get_pic_of_day(ENV))
    print(get_notifications(ENV))
    print(get_body_positions(ENV, 53, 0))
    star_charts = get_star_charts(ENV, 53, 0)
    print(star_charts[0])
    print(star_charts[1])
