DROP SCHEMA IF EXISTS astro_project CASCADE;
CREATE SCHEMA astro_project;
SET SEARCH_PATH TO astro_project;

CREATE TABLE neo (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    est_diameter_min BIGINT,
    est_diameter_max BIGINT,
    image_url TEXT,
    is_hazard BOOLEAN,
    is_sentry BOOLEAN,
    PRIMARY KEY(id)
);

CREATE TABLE close_approach (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    timestamp TIMESTAMP NOT NULL,
    neo_id BIGINT NOT NULL,
    relative_velocity BIGINT,
    approach_distance BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(neo_id) REFERENCES neo(id)
);

CREATE TABLE news_article (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    headline TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT,
    date TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE TABLE event (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    event_type VARCHAR(30) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    details TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE daily_image (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    title TEXT,
    potd_url TEXT NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE observer_region (
    id SMALLINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE observer_location (
    id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    region_id SMALLINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(region_id) REFERENCES observer_region(id)
);

CREATE TABLE weather (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    weather VARCHAR(30) NOT NULL,
    cloud_cover INT NOT NULL,
    temperature INT NOT NULL,
    visibility INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    location_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(location_id) REFERENCES observer_location(id)
);

CREATE TABLE aurora_status (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    colour VARCHAR(10) NOT NULL,
    status TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE sky (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    region_id SMALLINT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    aurora_value INT NOT NULL,
    aurora_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(region_id) REFERENCES observer_region(id),
    FOREIGN KEY(aurora_id) REFERENCES aurora_status(id)
);

CREATE TABLE constellation (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    code CHAR(3) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE constellation_sky (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    constellation_id BIGINT NOT NULL,
    sky_id BIGINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(constellation_id) REFERENCES constellation(id),
    FOREIGN KEY(sky_id) REFERENCES sky(id)
);

CREATE TABLE star_chart (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    default_url TEXT NOT NULL,
    red_url TEXT NOT NULL,
    constellation_id BIGINT NOT NULL,
    sky_id BIGINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(constellation_id) REFERENCES constellation(id),
    FOREIGN KEY(sky_id) REFERENCES sky(id)
);

CREATE TABLE celestial_body (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    right_ascension FLOAT NOT NULL,
    declination FLOAT NOT NULL,
    earth_dist BIGINT NOT NULL,
    constellation_id BIGINT NOT NULL,
    sky_id BIGINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(constellation_id) REFERENCES constellation(id),
    FOREIGN KEY(sky_id) REFERENCES sky(id)
);