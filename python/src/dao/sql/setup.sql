-- Create the schema
CREATE SCHEMA IF NOT EXISTS strava_api;

-- Create the athlete table
CREATE TABLE IF NOT EXISTS strava_api.athlete (
    athlete_id BIGINT PRIMARY KEY,
    athlete_name VARCHAR(255) NOT NULL,
    refresh_token VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Create the activities table
CREATE TABLE IF NOT EXISTS strava_api.activities (
    athlete_id BIGINT NOT NULL,
    athlete VARCHAR(255) NOT NULL,
    activity_id BIGINT PRIMARY KEY,
    run VARCHAR(255),
    moving_time INTERVAL,
    distance_mi FLOAT,
    pace_min_mi INTERVAL,
    full_date DATE,
    time TIME,
    day VARCHAR(3),
    month INT,
    date INT,
    year INT,
    spm_avg FLOAT,
    hr_avg FLOAT,
    wkt_type INT,
    description TEXT,
    total_elev_gain_ft FLOAT,
    manual BOOLEAN,
    max_speed_ft_s FLOAT,
    calories FLOAT,
    achievement_count INT,
    kudos_count INT,
    comment_count INT,
    athlete_count INT,
    full_datetime TIMESTAMP,
    rpe INT,
    rating INT,
    avg_power INT,
    sleep_rating INT,
    CONSTRAINT fk_athlete
        FOREIGN KEY (athlete_id)
        REFERENCES strava_api.athlete (athlete_id)
        ON DELETE CASCADE
);