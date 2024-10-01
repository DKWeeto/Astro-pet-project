from os import environ as ENV
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


def theming():
    selected = st.session_state['themebutton']
    if selected == 'light':
        st._config.set_option(f'theme.base', "dark")
        st._config.set_option(f'theme.backgroundColor', "#000000")
        st._config.set_option(f'theme.primaryColor', "#8B0000")
        st._config.set_option(f'theme.secondaryBackgroundColor', "#000000")
        st._config.set_option(f'theme.textColor', "#8B0000")
        st.session_state['themebutton'] = 'dark'
    else:
        st._config.set_option(f'theme.base', "light")
        st._config.set_option(f'theme.backgroundColor', "#FFFFFF")
        st._config.set_option(f'theme.primaryColor', "#000000")
        st._config.set_option(f'theme.secondaryBackgroundColor', "#AE74E0")
        st._config.set_option(f'theme.textColor', "#000000")
        st.session_state['themebutton'] = 'light'


def init_themes():
    if 'themebutton' not in st.session_state:
        st.session_state.themebutton = 'dark'

    with st.sidebar:
        st.button("Change theme", on_click=theming)


@st.cache_resource
def connect_to_db(config: dict) -> connection:
    """Returns a live database connection."""
    return connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=config["DB_PORT"]
    )


def get_daily_image(conn: connection, config: dict):
    sql_query = f"""SELECT potd_url, title, date
                FROM {config["SCHEMA_NAME"]}.daily_image
                ORDER BY date DESC
                LIMIT 1;"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        potd = cur.fetchone()
    return potd["potd_url"], potd["title"], potd["date"]


def get_neos(conn: connection, config: dict):
    sql_query = f"""SELECT n.name, c.timestamp, n.est_diameter_min, n.est_diameter_max, n.is_hazard, n.is_sentry
                FROM {config["SCHEMA_NAME"]}.neo as n
                JOIN {config["SCHEMA_NAME"]}.close_approach as c
                ON (n.id = c.neo_id)
                WHERE c.timestamp > CURRENT_TIMESTAMP
                ORDER BY c.timestamp;"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        neos = cur.fetchall()
    return neos


if __name__ == "__main__":
    init_themes()
    with connect_to_db(dict(ENV)) as conn:
        potd, title, date = get_daily_image(conn, ENV)
    st.markdown(f"## NASA's image of the day: {date}")
    st.markdown(
        f"<h4 style='text-align: center;'><i>{title}</i></h4>", unsafe_allow_html=True)
    if 'youtube' in potd:
        st.video(potd)
    else:
        st.image(potd, width=750)
    st.markdown(
        "NEOs, planet metadata/ fun facts, could combine upcoming events into here too")
    st.markdown("## Near Earth Objects")
    with connect_to_db(dict(ENV)) as conn:
        neos = get_neos(conn, ENV)
    st.table(pd.DataFrame(neos))
    st.markdown("## Meteor shower timetable")
