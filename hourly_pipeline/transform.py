from datetime import datetime

WEATHER_CODES = {0:	"Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                 45: "Fog", 48: "Depositing rime fog", 51: "Light Drizzle", 53: "Moderate Drizzle",
                 55: "Dense Drizzle", 56: "Light Freezing Drizzle", 57: "Dense Freezing Drizzle",
                 61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
                 66: "Light Freezing Rain", 67: "Heavy Freezing Rain", 71: "Slight Snowfall",
                 73: "Moderate Snowfall", 75: "Heavy Snowfall", 77: "Snow grains",
                 80: "Slight Rain Showers", 81: "Moderate Rain Showers", 82: "Violent Rain Showers",
                 85: "Slight Snow Showers", 86: "Heavy Snow Showers", 95: "Thunderstorm",
                 96: "Thunderstorm with Slight Hail", 99: "Thunderstorm with Heavy Hail"}


def format_data(data: dict) -> dict:
    formatted_data = {}
    for i, time in enumerate(data["time"]):
        weather = WEATHER_CODES[int(data["weather_code"][i])]
        formatted_data[datetime.strptime(time, "%Y-%m-%dT%H:%M")] = {"cloud_cover": int(round(data["cloud_cover"][i])),
                                                                     "temperature": int(round(data["temperature_2m"][i])),
                                                                     "visibility": int(round(data["visibility"][i])),
                                                                     "weather": weather}
    return formatted_data


def get_relevant_aurora_info(data):
    colour = data["state"]["@name"]
    if colour == "green":
        status_id = 1
    elif colour == "amber":
        status_id = 2
    elif colour == "yellow":
        status_id = 3
    elif colour == "red":
        status_id = 4
    return {"time": datetime.now().replace(minute=0).isoformat(timespec="minutes"), "value": data["state"]["@value"], "status_id": status_id}
