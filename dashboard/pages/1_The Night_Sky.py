from os import environ as ENV
import pandas as pd
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st
import altair as alt
from datetime import datetime, timedelta

DARK = """{"theme.base": "light",
        "theme.backgroundColor": "#000000",
        "theme.primaryColor": "#8B0000",
        "theme.secondaryBackgroundColor": "#000000",
        "theme.textColor": "#8B0000",
        "theme.font": "sans serif"}"""

LIGHT = """{"theme.base": "dark",
         "theme.backgroundColor": "#96DED1",
         "theme.primaryColor": "#c98bdb",
         "theme.secondaryBackgroundColor": "#96DED1",
         "theme.textColor": "#c98bdb",
         "theme.font": "sans serif"}"""


@st.cache_resource
def connect_to_db(config: dict) -> connection:
    """Returns a live database connection."""
    return connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=config["DB_PORT"],
        cursor_factory=RealDictCursor
    )


def get_regions(conn: connection, config):
    sql_query = f"""SELECT name from {config["SCHEMA_NAME"]}.observer_region"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        regions = cur.fetchall()
    return ['Please select a region'] + [region['name'] for region in regions]


def get_locations(conn, config, region_name):
    sql_query = f"""SELECT l.name FROM {config["SCHEMA_NAME"]}.observer_location as l
                    JOIN {config["SCHEMA_NAME"]}.observer_region as r
                    ON (l.region_id = r.id)
                    WHERE r.name = '{region_name}'"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        locations = cur.fetchall()
    return ['Please select a location'] + [location['name'] for location in locations]


def get_celestial_bodies(conn: connection, config: dict, region_name):
    now = datetime.now()
    if now.hour < 5:
        tomorrow = now.date()
        date = now.date() - timedelta(days=1)
    else:
        date = now.date()
        tomorrow = date + timedelta(days=1)
    sql_query = f"""SELECT b.name, b.altitude, b.azimuth, c.name as constellation, s.timestamp
                FROM {config["SCHEMA_NAME"]}.celestial_body AS b
                JOIN {config["SCHEMA_NAME"]}.constellation AS c
                ON (b.constellation_id = c.id)
                JOIN {config["SCHEMA_NAME"]}.sky AS s
                ON (b.sky_id = s.id)
                JOIN {config["SCHEMA_NAME"]}.observer_region AS o
                ON (s.region_id = o.id)
                WHERE o.name = '{region_name}'
                AND s.timestamp > '{date} 19:00'
                AND s.timestamp < '{tomorrow} 6:00'
                AND b.altitude > 0
                ORDER BY s.timestamp;"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        bodies = cur.fetchall()
    return bodies


def get_red_star_charts(conn: connection, config: dict, region_name):
    now = datetime.now()
    red_star_charts = []
    if now.hour < 5:
        date = now.date() - timedelta(days=1)
    else:
        date = now.date()
    sql_query = f"""SELECT s.red_url, c.name
                FROM {config["SCHEMA_NAME"]}.star_chart AS s
                JOIN {config["SCHEMA_NAME"]}.constellation AS c
                ON (s.constellation_id = c.id)
                JOIN {config["SCHEMA_NAME"]}.observer_region AS o
                ON (s.region_id = o.id)
                WHERE o.name = '{region_name}'
                AND s.date = '{date}';"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        red_charts = cur.fetchall()
    for chart in red_charts:
        red_star_charts.append((chart["red_url"], chart["name"]))
    return red_star_charts


def get_default_star_charts(conn: connection, config: dict, region_name):
    now = datetime.now()
    def_star_charts = []
    if now.hour < 5:
        date = now.date() - timedelta(days=1)
    else:
        date = now.date()
    sql_query = f"""SELECT s.default_url, c.name
                FROM {config["SCHEMA_NAME"]}.star_chart AS s
                JOIN {config["SCHEMA_NAME"]}.constellation AS c
                ON (s.constellation_id = c.id)
                JOIN {config["SCHEMA_NAME"]}.observer_region AS o
                ON (s.region_id = o.id)
                WHERE o.name = '{region_name}'
                AND s.date = '{date}';"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        def_charts = cur.fetchall()
    for chart in def_charts:
        def_star_charts.append((chart["default_url"], chart["name"]))
    return def_star_charts


def display_chart():
    chart = st.session_state.charts[st.session_state.count]
    st.markdown(
        f"<h4 style='text-align: center;'>{chart[1]}</h4>", unsafe_allow_html=True)
    st.markdown(
        f'<img src="{chart[0]}" alt="Red star chart" width="650"/>', unsafe_allow_html=True)


def next_chart():
    if st.session_state.count + 1 >= len(st.session_state.charts):
        st.session_state.count = 0
    else:
        st.session_state.count += 1


def previous_chart():
    if st.session_state.count > 0:
        st.session_state.count -= 1
    else:
        st.session_state.count = len(st.session_state.charts) - 1


def star_charts(config, region_name):
    with connect_to_db(config) as conn:
        if st.session_state.themebutton == "dark":
            charts_list = get_red_star_charts(conn, config, region_name)
        else:
            charts_list = get_default_star_charts(conn, config, region_name)
    if charts_list:
        if 'charts' not in st.session_state or st.session_state.charts != charts_list:
            st.session_state.count = 0
            st.session_state.charts = charts_list

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("← Previous", key="p_chart", on_click=previous_chart):
                pass

        with col5:
            if st.button("Next →", key="n_chart", on_click=next_chart):
                pass

        display_chart()
    else:
        st.markdown("##### No star charts right now, check back later!")


def weather_forecast(conn, config, location_name):
    now = datetime.now()
    if now.hour < 5:
        tomorrow = now.date()
        date = now.date() - timedelta(days=1)
    else:
        date = now.date()
        tomorrow = date + timedelta(days=1)
    sql_query = f"""SELECT cast(w.timestamp as time) as "Time", l.name as "Location", w.weather as "Weather",
                w.cloud_cover as "Cloud cover", w.temperature as "Temperature", w.visibility/ 24140 * 100 as "Visibility"
                FROM {config["SCHEMA_NAME"]}.weather as w
                JOIN {config["SCHEMA_NAME"]}.observer_location as l
                ON (w.location_id = l.id)
                WHERE l.name = '{location_name}'
                AND w.timestamp > '{date} 19:00'
                AND w.timestamp < '{tomorrow} 6:00'
                ORDER BY w.timestamp;"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        weather = cur.fetchall()
    return weather


def aurora_status(conn: connection, config: dict, region_name):
    sql_query = f"""SELECT * FROM (SELECT s.timestamp as "Timestamp", s.aurora_value as "Value", a.colour as "Alert", a.status as "Status"
                FROM {config["SCHEMA_NAME"]}.sky AS s
                JOIN {config["SCHEMA_NAME"]}.observer_region AS o
                ON (s.region_id = o.id)
                JOIN {config["SCHEMA_NAME"]}.aurora_status AS a
                ON (s.aurora_id = a.id)
                WHERE o.name = '{region_name}'
                AND s.timestamp < CURRENT_TIMESTAMP
                ORDER BY s.timestamp DESC
                LIMIT 10) ORDER BY "Timestamp";"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_query)
        auroras = cur.fetchall()
    return auroras


def get_bodies_list(config, region_name):
    with connect_to_db(dict(ENV)) as conn:
        bodies = get_celestial_bodies(conn, config, region_name)
    if bodies:
        bodies = pd.DataFrame(bodies)
        sun_in_sky = bodies[bodies["name"] == "Sun"]["timestamp"]
        bodies = bodies[~bodies["timestamp"].isin(sun_in_sky)]
        bodies["azimuth"] = bodies["azimuth"].apply(lambda x: int(x))
        bodies = bodies.groupby("name")
        bodies = [{x: bodies.get_group(x)[["altitude", "azimuth", "constellation", "timestamp"]].to_dict(
            "split", index=False)['data']} for x in bodies.groups]
    return bodies


def display_body():
    body = st.session_state.bodies[st.session_state.b_count]
    body_name = list(body.keys())[0]
    if body_name in ["Waxing Crescent", "Waning Crescent", "Waxing Gibbous", "Waning Gibbous", "First Quarter", "Third Quarter", "Full", "New"]:
        body_name = f"The Moon: {body_name}"
    items = list(body.values())[0]
    st.title(body_name)
    for event in items:
        altitude, azimuth, constellation, timestamp = event
        # change this to like a drop down or widget or metric or something for each time
        with st.container(border=True):
            st.markdown(
                f"<h4 style='text-align: left;'>At: {timestamp}</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1.container(border=True):
                st.markdown(
                    f"<h5 style='text-align: center;'>Altitude: {altitude}°</h5>", unsafe_allow_html=True)
            with col2.container(border=True):
                st.markdown(
                    f"<h5 style='text-align: center;'>Direction: {azimuth}°</h5>", unsafe_allow_html=True)
            with col3.container(border=True):
                st.markdown(
                    f"<h5 style='text-align: center;'>Constellation: {constellation}</h5>", unsafe_allow_html=True)
    # st.markdown(
    #     f'<img src="{body}" alt="Celestial body image" width="650"/>', unsafe_allow_html=True)


def next_body():
    if st.session_state.b_count + 1 >= len(st.session_state.bodies):
        st.session_state.b_count = 0
    else:
        st.session_state.b_count += 1


def previous_body():
    if st.session_state.b_count > 0:
        st.session_state.b_count -= 1
    else:
        st.session_state.b_count = len(st.session_state.bodies) - 1


def body_info(config, region_name):
    bodies = get_bodies_list(config, region_name)
    if bodies:
        if "bodies" not in st.session_state or st.session_state.bodies != bodies:
            st.session_state.b_count = 0
            st.session_state.bodies = bodies

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("← Previous", key="p_body", on_click=previous_body):
                pass

        with col5:
            if st.button("Next →", key="n_body", on_click=next_body):
                pass

        display_body()
    else:
        st.markdown("##### No sky data right now, check back later!")


def aurora_graph(aurora_data):
    if st.session_state.themebutton == "dark":
        main_color = "#8B0000"
        color_range = ['#800020', '#8B0000', '#A52A2A', '#D22B2B']
        rules = alt.Chart(pd.DataFrame({'y': [50, 100, 200]})).mark_rule(color=main_color).encode(
            y='y',
            tooltip=alt.value("Yellow alert threshold")
        )
    else:
        main_color = "#000000"
        color_range = ['green', 'yellow', 'orange', 'red']
        yellow_chart = alt.Chart(pd.DataFrame({'y': [50]})).mark_rule(color='yellow').encode(
            y='y',
            tooltip=alt.value("Yellow alert threshold")
        )
        amber_chart = alt.Chart(pd.DataFrame({'y': [100]})).mark_rule(color='orange').encode(
            y='y',
            tooltip=alt.value("Amber alert threshold")
        )
        red_chart = alt.Chart(pd.DataFrame({'y': [200]})).mark_rule(color='red').encode(
            y='y',
            tooltip=alt.value("Red alert threshold")
        )
        rules = yellow_chart+amber_chart+red_chart
    aurora_chart = alt.Chart(aurora_data).mark_bar(color=main_color, size=55).encode(
        x=alt.X('Timestamp:T', axis=alt.Axis(
            format='%H:%M:%S'), title="Time"),
        y=alt.Y('Value:Q', title="Activity (nT)"),
        color=alt.Color('Alert', scale=alt.Scale(range=color_range, domain=[
            'Green', 'Yellow', 'Amber', 'Red']))
    )

    combined_aurora = aurora_chart+rules
    st.altair_chart(combined_aurora.configure_axis(
        tickColor=main_color,
        labelColor=main_color,
        titleColor=main_color,
        domainColor=main_color,
        grid=False).configure_legend(
        labelColor=main_color,
        titleColor=main_color), use_container_width=True)


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


if __name__ == "__main__":
    load_dotenv()
    init_themes()

    with connect_to_db(dict(ENV)) as conn:
        regions = get_regions(conn, ENV)
    region = st.selectbox('Regions', regions)
    if region != 'Please select a region':
        st.markdown("## What's in the sky tonight?")
        body_info(ENV, region)
        st.markdown("## Star charts")
        star_charts(dict(ENV), region)

        st.markdown("## Weather forecast")
        with connect_to_db(dict(ENV)) as conn:
            locations = get_locations(conn, ENV, region)
        location = st.selectbox('Locations', locations)
        if location != 'Please select a location':
            st.markdown(f"### Tonight in {location}")
            with connect_to_db(dict(ENV)) as conn:
                weather = pd.DataFrame(weather_forecast(conn, ENV, location))[[
                    'Time', 'Location', 'Weather', 'Cloud cover', 'Temperature']]
                weather['Cloud cover'] = weather['Cloud cover'].apply(
                    lambda x: str(x) + '%')
                weather['Temperature'] = weather['Temperature'].apply(
                    lambda x: str(x) + '°C')
            st.table(weather)

        st.markdown("## Aurora Watch UK")
        with connect_to_db(dict(ENV)) as conn:
            auroras = pd.DataFrame(aurora_status(conn, ENV, region))
        aurora_graph(auroras)
