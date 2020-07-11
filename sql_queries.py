import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays" 
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE staging_events(
    artist_name VARCHAR,
    auth VARCHAR,
    user_first_name VARCHAR,
    user_gender  VARCHAR,
    item_in_session INT,
    user_last_name VARCHAR,
    song_length FLOAT, 
    user_level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    session_id INT,
    song_title VARCHAR,
    status INT,
    ts VARCHAR,
    user_agent TEXT,
    user_id VARCHAR)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs(
    song_id  VARCHAR PRIMARY KEY,
    num_songs INT,
    artist_id  VARCHAR,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location VARCHAR,
    artist_name VARCHAR,
    title VARCHAR,
    duration FLOAT,
    year INT)
""")

songplay_table_create = ( """
CREATE TABLE songplays(
    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time TIMESTAMP,
    user_id VARCHAR,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location VARCHAR,
    user_agent TEXT,
    UNIQUE (start_time, user_id, song_id, artist_id))
""")


user_table_create = ("""
CREATE TABLE users(
user_id VARCHAR PRIMARY KEY,
first_name VARCHAR,
last_name VARCHAR,
gender VARCHAR,
level VARCHAR)
""")

song_table_create = ("""
CREATE TABLE songs(
song_id VARCHAR PRIMARY KEY,
title VARCHAR,
artist_id VARCHAR,
year INT,
duration float)
""")

artist_table_create = ("""
CREATE TABLE artists(
artist_id VARCHAR PRIMARY KEY,
name TEXT,
location VARCHAR,
latitude FLOAT,
longitude FLOAT)
""")

time_table_create = ("""CREATE TABLE time(
start_time TIMESTAMP PRIMARY KEY,
hour INT,
day INT,
week INT,
month INT,
year INT,
weekday INT)
""")

# STAGING TABLES
#Iam not sure
staging_events_copy = ("""copy staging_events from '{}'
 credentials 'aws_iam_role={}'
 region 'us-west-2' 
 COMPUPDATE OFF STATUPDATE OFF
 JSON '{}'""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'),config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs from '{}'
    credentials 'aws_iam_role={}'
    region 'us-west-2' 
    COMPUPDATE OFF STATUPDATE OFF
    JSON 'auto' """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    SELECT DISTINCT 
        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time, 
        v.user_id, 
        v.user_level,
        so.song_id,
        so.artist_id,
        v.session_id,
        v.location,
        v.user_agent
    FROM staging_events v, staging_songs so
    WHERE v.page = 'NextSong'
    AND v.song_title = so.title
    AND user_id NOT IN (SELECT DISTINCT s.user_id FROM songplays s WHERE s.user_id = user_id
                       AND s.start_time = start_time AND s.session_id = session_id )
""")


user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)  
    SELECT DISTINCT user_id, user_first_name, user_last_name, user_gender, user_level
    FROM staging_events
    WHERE page = 'NextSong'
    AND user_id NOT IN (SELECT DISTINCT user_id FROM users)
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs
    WHERE song_id NOT IN (SELECT DISTINCT song_id FROM songs)
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs
    WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artists)
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT start_time, 
        EXTRACT(hour from start_time) AS hour,
        EXTRACT(day from start_time) AS day,
        EXTRACT(week from start_time) AS week,
        EXTRACT(month from start_time) AS month,
        EXTRACT(year from start_time) AS year, 
        EXTRACT(weekday from start_time) AS weekday 
    FROM (SELECT DISTINCT  TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time 
        FROM staging_events s )
    WHERE start_time NOT IN (SELECT DISTINCT start_time FROM time)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
