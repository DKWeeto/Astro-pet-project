"""Load"""

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


def get_region_id(schema, conn: connection, latitude: float, longitude: float) -> int:
    """Returns the location ID for a given latitude and longitude."""

    sql_query = f"""
        SELECT id
        FROM {schema}.observer_region
        WHERE latitude = {latitude}
        AND longitude = {longitude};
        """

    with conn.cursor() as cur:
        cur.execute(sql_query)
        location_id = cur.fetchone()["id"]

    return location_id


def update_approach_data(schema, conn: connection, data, approach_id):
    """Update existing approach data"""
    sql_query = f"""
        UPDATE {schema}.close_approach AS c
        SET
        relative_velocity = u.velocity,
        approach_distance = u.distance
        FROM (VALUES
        ({approach_id}, {data["relative_velocity"]}, {data["approach_dist"]})
        )
        AS u(id, velocity, distance)
        WHERE c.id = u.id;
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def insert_approach_data(schema: str, conn: connection, data: dict, neo_id):
    """Load new approach data"""
    sql_query = f"""
        INSERT INTO {schema}.close_approach (timestamp, relative_velocity, approach_distance, neo_id)
        VALUES
        ('{data["timestamp"]}',
        {data["relative_velocity"]},
        {data["approach_dist"]},
        {neo_id});
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def insert_neo_data(schema: str, conn: connection, data: dict) -> int:
    """Load neo data"""
    sql_query = f"""
        INSERT INTO {schema}.neo (name, est_diameter_min, est_diameter_max, is_hazard, is_sentry)
        VALUES
        ('{data["name"]}',
        {data["est_diameter_min"]},
        {data["est_diameter_max"]},
        {data["is_hazard"]},
        {data["is_sentry"]})
        RETURNING id;
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()
        neo_id = cur.fetchone()
    return neo_id['id']


def check_if_existing_neo(schema, conn, name):
    """Check if neo exists in db"""
    sql_query = f"""
                SELECT id FROM {schema}.neo
                WHERE name = '{name}'
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        neo_id = cur.fetchone()
    return neo_id


def check_if_existing_approach(schema, conn, timestamp, neo_id):
    """Check if approach exists in db"""
    sql_query = f"""
                SELECT id FROM {schema}.close_approach
                WHERE timestamp = '{timestamp}'
                AND neo_id = {neo_id}
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        approach_id = cur.fetchone()
    return approach_id


def enter_approach_updates(schema, conn, neo_data: list):
    """Load approach data"""
    for neo in neo_data:
        neo_id = check_if_existing_neo(schema, conn, neo["name"])
        for approach in neo['approaches']:
            if neo_id:
                approach_id = check_if_existing_approach(
                    schema, conn, approach['timestamp'], neo_id["id"])
                if not approach_id:
                    insert_approach_data(schema, conn, approach, neo_id["id"])
            else:
                neo_id = insert_neo_data(schema, conn, neo)
                insert_approach_data(schema, conn, approach, neo_id)


def enter_daily_image(schema, conn, image_data: dict):
    """Load image of the day"""
    sql_query = f"""
        INSERT INTO {schema}.daily_image (potd_url, title, date)
        VALUES
        ('{image_data["url"]}',
        '{image_data["title"].replace("'", "")}',
        '{image_data["date"]}');
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def check_if_existing_notification(schema, conn, notif_data):
    """Check if notifications exists in db"""
    sql_query = f"""
                SELECT id FROM {schema}.notification
                WHERE message_type = '{notif_data["type"]}'
                AND summary = '{notif_data["summary"]}';
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        notif_id = cur.fetchone()
    return notif_id


def insert_notification(schema: str, conn: connection, notif_data: dict):
    """Insert a new notification"""
    sql_query = f"""
        INSERT INTO {schema}.notification (message_type, summary)
        VALUES
        ('{notif_data["type"]}',
        '{notif_data["summary"]}');
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def enter_notifications(schema, conn: connection, notification_data):
    """Insert all notifications"""
    for notification in notification_data:
        notif_id = check_if_existing_notification(schema, conn, notification)
        if not notif_id:
            insert_notification(schema, conn, notification)


def check_if_existing_sky(schema, conn, region_id, time):
    """Check if sky data in db"""
    sql_query = f"""
                SELECT id FROM {schema}.sky
                WHERE region_id = {region_id}
                AND timestamp = '{time}'
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        sky_id = cur.fetchone()
    return sky_id


def get_constellation_id(schema, conn, constellation_code):
    """Extract constellation id"""
    sql_query = f"""
                SELECT id FROM {schema}.constellation
                WHERE code = '{constellation_code}';
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        constellation_id = cur.fetchone()
    return constellation_id


def insert_celestial_body(schema: str, conn: connection, body_data: dict, sky_id, constellation_id):
    """Insert info for a celestial body"""
    sql_query = f"""
        INSERT INTO {schema}.celestial_body (name, altitude, azimuth, earth_dist, sky_id, constellation_id)
        VALUES
        ('{body_data["name"]}',
        {body_data["altitude"]},
        {body_data["azimuth"]},
        {body_data["earth_dist"]},
        {sky_id},
        {constellation_id});
        """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def enter_celestial_bodies(schema, conn: connection, region_id, body_data):
    """Check if a sky entry exists, add it if not,
    get the sky_id and constellation_id from database
    Insert tonights celestial bodies."""
    for body in body_data:
        sky_id = check_if_existing_sky(
            schema, conn, region_id, body["date"])
        if sky_id:
            sky_id = sky_id["id"]
        else:
            sql_query = f"""
            INSERT INTO {schema}.sky (region_id, timestamp, aurora_value, aurora_id)
            VALUES
            ({region_id},
            '{body["date"]}',
            0,
            1)
            RETURNING id;
            """
            with conn.cursor() as cur:
                cur.execute(sql_query)
                conn.commit()
                sky_id = cur.fetchone()["id"]
        constellation_id = get_constellation_id(
            schema, conn, body["constellation_code"])["id"]
        insert_celestial_body(schema, conn, body, sky_id, constellation_id)


def insert_star_chart(schema: str, conn: connection, star_chart):
    """Load a star chart into db"""
    sql_query = f"""
        INSERT INTO {schema}.star_chart (red_url, default_url, constellation_id, date, region_id)
        VALUES (
        '{star_chart["red_url"]}',
        '{star_chart["default_url"]}',
        {star_chart["constellation_id"]},
        '{star_chart["date"]}',
        {star_chart["region_id"]}
        );"""
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def enter_star_charts(schema, conn: connection, star_charts):
    """Load all star charts into db"""
    for star_chart in star_charts:
        insert_star_chart(schema, conn, star_chart)
