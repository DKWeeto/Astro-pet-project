from os import environ as ENV
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st


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


def get_notifications(conn: connection, config: dict):
    sql_query = f"""SELECT message_type, summary from {config["SCHEMA_NAME"]}.notification;"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        notifs = cur.fetchall()
    return [(notif["message_type"].replace("#", ""), notif["summary"].replace("#", "")) for notif in notifs]


if __name__ == "__main__":
    init_themes()
    load_dotenv()
    with connect_to_db(dict(ENV)) as conn:
        notifications = get_notifications(conn, ENV)
    # TODO: what do i even do with this, might be useless
    for notification in notifications:
        st.markdown(f"# {notification[0]}")
        st.markdown(f"{notification[1]}")
