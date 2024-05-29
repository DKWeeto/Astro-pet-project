from os import environ as ENV
from dotenv import load_dotenv
from datetime import datetime
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(config: dict) -> connection:
    """Returns a connection to the database."""

    return connect(
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        database=config["DB_NAME"],
        cursor_factory=RealDictCursor
    )


def get_location_id(schema, conn: connection, latitude: float, longitude: float) -> int:
    """Returns the location ID for a given latitude and longitude."""

    sql_query = f"""
        SELECT id
        FROM {schema}.observer_location
        WHERE latitude = {latitude}
        AND longitude = {longitude};
        """

    with conn.cursor() as cur:
        cur.execute(sql_query)
        location_id = cur.fetchone()["id"]

    return location_id


def change_existing(schema, conn: connection, time, data, weather_id):
    sql_query = f"""
        UPDATE {schema}.weather AS w
        SET
        cloud_cover = u.new_cloud,
        temperature = u.new_temp,
        visibility = u.new_vis,
        weather = u.new_weather
        FROM (VALUES
        ({weather_id}, {data["cloud_cover"]}, {data["temperature"]}, {data["visibility"]}, '{data["weather"]}')
        )
        AS u(id, new_cloud, new_temp, new_vis, new_weather)
        WHERE w.timestamp = '{time}'
        AND w.id = u.id;
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def insert_new_data(schema, conn: connection, time, data, location_id):
    sql_query = f"""
        INSERT INTO {schema}.weather (cloud_cover, temperature, visibility, weather, location_id, timestamp)
        VALUES
        ({data["cloud_cover"]},
        {data["temperature"]},
        {data["visibility"]},
        '{data["weather"]}',
        {location_id},
        '{time}');
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def check_if_existing(schema, conn, location_id, time):
    sql_query = f"""
                SELECT id FROM {schema}.weather
                WHERE location_id = {location_id}
                AND timestamp = '{time}'
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        weather_id = cur.fetchone()
    return weather_id


def enter_weather_updates(schema, conn, location_id, data: dict):
    for time in data.keys():
        id = check_if_existing(schema, conn, location_id, time)
        if id:
            change_existing(schema, conn, time, data[time], id["id"])
        else:
            insert_new_data(schema, conn, time, data[time], location_id)


def enter_sky_update(schema, conn, region_id, aurora_info):
    sql_query = f"""
        INSERT INTO {schema}.sky (region_id, timestamp, aurora_value, aurora_id)
        VALUES
        ({region_id},
        '{aurora_info["time"]}',
        {aurora_info["value"]},
        {aurora_info["status_id"]});
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()
