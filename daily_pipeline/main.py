"""ETL"""

from os import environ as ENV
from datetime import datetime, timedelta
from requests import exceptions

from dotenv import load_dotenv

import extract as ex
import transform as tr
import load as lo


def location_pipeline(config, region_id, latitude, longitude):
    """ETL location based data"""
    body_data = tr.format_body_positions(
        ex.get_body_positions(config, latitude, longitude))

    with lo.get_db_connection(config) as conn:
        lo.enter_celestial_bodies(
            config["SCHEMA_NAME"], conn, region_id, body_data)
        constellations = get_constellations(config)
        star_charts = []
        for constellation in constellations:
            try:
                red, default = ex.get_star_charts(
                    config, latitude, longitude, constellation[1])
                if 'data' in red and 'data' in default:
                    star_charts.append(tr.get_star_chart_data(
                        red, default, constellation[0], region_id))
            except exceptions.ReadTimeout:
                print(f"Time out error for location: {region_id}")

        if star_charts:
            lo.enter_star_charts(config["SCHEMA_NAME"],
                                 conn, star_charts)
    conn.close()


def get_lats_lons(config) -> list[tuple[float]]:
    """Get all latitudes and longitudes from db"""
    with lo.get_db_connection(config) as conn:
        sql_query = f"""
                        SELECT id, latitude, longitude FROM {config["SCHEMA_NAME"]}.observer_region
                        """
        with conn.cursor() as cur:
            cur.execute(sql_query)
            locations = [(row["id"], row["latitude"], row["longitude"])
                         for row in cur.fetchall()]
    return locations


def get_constellations(config) -> set[tuple[float]]:
    """ETL constellations"""
    with lo.get_db_connection(config) as conn:
        sql_query = f"""
                        SELECT c.id, c.code FROM {config["SCHEMA_NAME"]}.constellation AS c
                        JOIN {config["SCHEMA_NAME"]}.celestial_body AS b
                        ON c.id = b.constellation_id
                        JOIN {config["SCHEMA_NAME"]}.sky AS s
                        ON s.id = b.sky_id
                        WHERE s.timestamp > '{datetime.now().date()} 19:00'
                        AND s.timestamp < '{datetime.now().date() + timedelta(days=1)} 05:00'
                        """
        with conn.cursor() as cur:
            cur.execute(sql_query)
            constellations = [(row["id"], row["code"])
                              for row in cur.fetchall()]
            if (77, 'uma') not in constellations:
                constellations.append((77, 'uma'))
            if (79, 'umi') not in constellations:
                constellations.append((79, 'umi'))
    return set(constellations)


def full_pipeline(config):
    """Extract, transform and load all data"""
    daily_image = tr.get_daily_image(ex.get_pic_of_day(config))
    print(daily_image)
    # notifications = get_notification_messages(get_notifications(config))
    neos = tr.transform_neo_data(ex.get_neos(config))
    with lo.get_db_connection(config) as conn:
        lo.enter_daily_image(config['SCHEMA_NAME'], conn, daily_image)
        # enter_notifications(config['SCHEMA_NAME'], conn, notifications)
        lo.enter_approach_updates(config['SCHEMA_NAME'], conn, neos)
    locations = get_lats_lons(config)
    for location in locations:
        location_pipeline(
            config, location[0], location[1], location[2])


if __name__ == "__main__":
    load_dotenv()
    print(datetime.now())
    full_pipeline(ENV)
