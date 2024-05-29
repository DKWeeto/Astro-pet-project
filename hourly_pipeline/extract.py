from datetime import datetime, timedelta
from requests import get


def get_weather(latitude: float, longitude: float) -> dict:
    """Returns a request object for the weather details for the upcoming or current night."""
    now = datetime.now().replace(second=0, microsecond=0, minute=0)
    if 4 <= now.hour < 20:
        start = now.replace(hour=20)
        end = start + timedelta(hours=8)
    else:
        start = now
        if now.hour >= 20:
            end = now.replace(hour=4) + timedelta(days=1)
        else:
            end = now.replace(hour=4)
    return get(
        f'https://api.open-meteo.com/v1/forecast?latitude={str(latitude)}&longitude={str(longitude)}&hourly=cloud_cover,temperature_2m,visibility,weather_code&start_hour={start.isoformat(timespec="minutes")}&end_hour={end.isoformat(timespec="minutes")}&timezone=Europe/London',
        timeout=6).json()["hourly"]


def get_aurora_status():
    ...
