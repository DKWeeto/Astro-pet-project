from os import environ as ENV
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime, timedelta


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


if __name__ == "__main__":
    init_themes()
    load_dotenv()
    st.markdown("## News articles")
    # TODO: make a news scraper innit
    st.markdown("TODO")
