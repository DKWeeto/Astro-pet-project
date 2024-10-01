#!/venv/bin/python

from os import environ as ENV

from dotenv import load_dotenv

from extract import get_weather, get_aurora_status
from transform import format_data, get_relevant_aurora_info
from load import get_db_connection, enter_weather_updates, enter_sky_update


def location_pipeline(config, location_id, latitude, longitude):
    data = format_data(get_weather(latitude, longitude))
    with get_db_connection(config) as conn:
        enter_weather_updates(config["SCHEMA_NAME"], conn, location_id, data)
    conn.close()


def get_lats_lons(config) -> list[tuple[float]]:
    with get_db_connection(config) as conn:
        sql_query = f"""
                        SELECT id, latitude, longitude FROM {config["SCHEMA_NAME"]}.observer_location
                        """
        with conn.cursor() as cur:
            cur.execute(sql_query)
            locations = [(row["id"], row["latitude"], row["longitude"])
                         for row in cur.fetchall()]
    return locations


def full_pipeline(config):
    locations = get_lats_lons(config)
    for location in locations:
        location_pipeline(config, location[0], location[1], location[2])
    aurora_info = get_relevant_aurora_info(get_aurora_status())
    with get_db_connection(config) as conn:
        for i in range(1, 13):
            enter_sky_update(config["SCHEMA_NAME"], conn, i, aurora_info)
    conn.close()


if __name__ == "__main__":
    load_dotenv()
    full_pipeline(ENV)
