"""Transform"""

from datetime import datetime


def transform_neo_data(data):
    """Clean data for Near Earth Objects"""
    transformed_data = []
    for date in data.keys():
        for neo in data[date]:
            approaches = [{"timestamp": datetime.strptime(approach["close_approach_date_full"],
                                                          "%Y-%b-%d %H:%M"),
                           "relative_velocity": round(float(
                               approach["relative_velocity"]["kilometers_per_second"]), 2),
                           "approach_dist": round(float(
                               approach["miss_distance"]["kilometers"]))}
                          for approach in neo["close_approach_data"]]

            transformed_data.append({"name": neo["name"],
                                     "est_diameter_min": round(float(
                                         neo["estimated_diameter"]["meters"]
                                            ["estimated_diameter_min"]), 2),
                                     "est_diameter_max": round(float(
                                         neo["estimated_diameter"]["meters"]
                                            ["estimated_diameter_max"]), 2),
                                     "is_sentry": neo["is_sentry_object"] == "true",
                                     "is_hazard": neo
                                     ["is_potentially_hazardous_asteroid"] == "true",
                                     "approaches": approaches})
    return transformed_data


def get_daily_image(data):
    """Transform NASA daily image"""
    if data['media_type'] == 'video':
        return {"url": data["url"], "title": data["title"], "date": data["date"]}
    return {"url": data["hdurl"], "title": data["title"], "date": data["date"]}


def get_star_chart_data(red_url, default_url, constellation_id, region_id):
    """Transform star chart images"""
    return {"red_url": red_url['data']['imageUrl'], "default_url": default_url['data']['imageUrl'],
            "constellation_id": constellation_id, "region_id": region_id,
            "date": datetime.now().date()}


def get_notification_messages(data):
    """Clean notification data"""
    # TODO: figure out better4 data
    notifications = []
    for message in data:
        message_body = message["messageBody"].strip()
        message_type = message_body.split('Message Type: ')[1].split('\n')[
            0].replace("'", "''")
        summary = message_body.split('Summary:')[1].split(
            "Activity ID")[0].split("## Notes:")[0].replace("'", "''")
        notifications.append({"type": message_type, "summary": summary})
    return notifications


def format_body_positions(data):
    """Clean celestial body data"""
    info_list = []
    for forecast in data:
        for item in forecast['data']['table']['rows']:
            item = item['cells'][0]
            date = datetime.strptime(
                item['date'].split('.000+')[0], "%Y-%m-%dT%H:%M:%S")
            name = item['name']
            if name == 'Moon':
                name = item['extraInfo']['phase']['string']
            if name != "Earth":
                alt = round(float(item['position']['horizontal']
                                  ['altitude']['degrees']), 2)
                azi = round(float(item['position']['horizontal']
                            ['azimuth']['degrees']))
                dist = round(float(item['distance']['fromEarth']['km']))
                const = item['position']['constellation']['id']
                info_list.append(
                    {"name": name, "altitude": alt, "azimuth": azi, "earth_dist": dist,
                     "constellation_code": const, "date": date})
    return info_list
