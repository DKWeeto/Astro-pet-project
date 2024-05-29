from extract import get_body_positions
from datetime import datetime
from os import environ as ENV
from dotenv import load_dotenv


def transform_neo_data(data):
    transformed_data = []
    for date in data.keys():
        for neo in date:
            approaches = [{"timestamp": datetime.strptime(approach["close_approach_date_full"], "%Y-%b-%d %H:%M"),
                           "relative_velocity": round(float(approach["relative_velocity"]["kilometers_per_second"]), 2),
                           "approach_dist": round(float(approach["miss_distance"]["kilometers"]))}
                          for approach in neo["close_approach_data"]]

            transformed_data.append({"name": neo["name"],
                                     "est_diameter_min": round(float(neo["estimated_diameter"]["meters"]["estimated_diameter_min"]), 2),
                                     "est_diameter_max": round(float(neo["estimated_diameter"]["meters"]["estimated_diameter_max"]), 2),
                                     "is_sentry": True if neo["is_sentry_object"] == "true" else False,
                                     "is_hazard": True if neo["is_potentially_hazardous_asteroid"] == "true" else False,
                                     "approaches": approaches})
    return transformed_data


def get_daily_image(data):
    return {"url": data["hdurl"], "title": data["title"]}


def get_notification_messages(data):
    notifications = []
    for message in data:
        message_body = message["messageBody"].strip()
        message_type = message_body.split('Message Type: ')[1].split('\n')[0]
        summary = message_body.split('Summary:')[1].split(
            "Activity ID")[0].split("## Notes:")[0]
        notifications.append({"type": message_type, "summary": summary})


def format_body_positions(data):
    info_list = []
    for item in data['data']['table']['rows']:
        item = item['cells'][0]
        date = datetime.strptime(
            item['date'].split('.000+')[0], "%Y-%m-%dT%H:%M:%S")
        name = item['name']
        if name == 'Moon':
            name = item['extraInfo']['phase']['string']
        ra = float(item['position']['equatorial']['rightAscension']['hours'])
        dec = float(item['position']['equatorial']['declination']['degrees'])
        dist = round(float(item['distance']['fromEarth']['km']))
        const = item['position']['constellation']['id']
        info_list.append(
            {"name": name, "right_ascension": ra, "declination": dec, "earth_dist": dist,
             "constellation_code": const, "date": date})
    return info_list


if __name__ == "__main__":
    load_dotenv()
    for hour in get_body_positions(ENV, 53, 0):
        print(format_body_positions(hour))
