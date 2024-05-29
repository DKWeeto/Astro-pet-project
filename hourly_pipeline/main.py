from os import environ as ENV

from dotenv import load_dotenv

from extract import get_weather
from transform import format_data
from load import get_db_connection, get_location_id, enter_weather_updates


def location_pipeline(config, latitude, longitude):
    data = format_data(get_weather(latitude, longitude))
    with get_db_connection(config) as conn:
        location_id = get_location_id(
            config["SCHEMA_NAME"], conn, latitude, longitude)
        enter_weather_updates(config["SCHEMA_NAME"], conn, location_id, data)
    conn.close()


def get_lats_lons(config) -> list[tuple[float]]:
    with get_db_connection(config) as conn:
        sql_query = f"""
                        SELECT latitude, longitude FROM {config["SCHEMA_NAME"]}.observer_location
                        """
        with conn.cursor() as cur:
            cur.execute(sql_query)
            locations = [(row["latitude"], row["longitude"])
                         for row in cur.fetchall()]
    return locations


def full_pipeline(config):
    locations = get_lats_lons(config)
    for location in locations:
        location_pipeline(config, location[0], location[1])


if __name__ == "__main__":
    load_dotenv()
    full_pipeline(ENV)
