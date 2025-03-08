from pyflink.table import EnvironmentSettings, StreamTableEnvironment
from sqlalchemy import create_engine, Column, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Define the base for declarative class definitions
Base = declarative_base()


# Create tables in PostgreSQL using SQLAlchemy
# Define the table structure using SQLAlchemy ORM
class WeatherSinkTable(Base):
    __tablename__ = "weather_sink_table"

    # Define primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    dt = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    precipitation = Column(Float, nullable=False)


# Define the table structure for hourly aggregated precipitation
class WeatherHourlyTable(Base):
    __tablename__ = "weather_hourly"

    # Define primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    event_hour = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    total_precipitation = Column(Float, nullable=False)


# Connect to PostgreSQL database
DATABASE_URL = "postgresql://flink:postgres@postgres:5432/postgres"
engine = create_engine(DATABASE_URL, echo=True)

# Create the tables in the database
Base.metadata.create_all(engine)


# Set up the StreamTableEnvironment in streaming mode
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = StreamTableEnvironment.create(environment_settings=env_settings)

# Kafka source configuration (unchanged)
table_env.execute_sql(
    """
    CREATE TABLE weather_source (
        lat DOUBLE,
        lon DOUBLE,
        minutely ARRAY<ROW<dt BIGINT, precipitation FLOAT>>,
        timezone STRING,
        timezone_offset INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'weather',
        'properties.bootstrap.servers' = 'kafka:29092',
        'properties.group.id' = 'weather_group',
        'format' = 'json',
        'scan.startup.mode' = 'latest-offset'
    )
    """
)

# PostgreSQL sink configuration for processed data (flattened)
table_env.execute_sql(
    """
    CREATE TABLE weather_sink (
        dt TIMESTAMP(3),
        precipitation FLOAT,
        WATERMARK FOR dt AS dt - INTERVAL '0' SECOND
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/postgres',
        'table-name' = 'weather_sink_table',
        'username' = 'flink',
        'password' = 'postgres',
        'driver' = 'org.postgresql.Driver',
        'sink.buffer-flush.max-rows' = '1000',
        'sink.buffer-flush.interval' = '1s'
    )
    """
)

# Create a new table for hourly aggregated precipitation (PostgreSQL sink)
table_env.execute_sql(
    """
    CREATE TABLE weather_hourly (
        event_hour TIMESTAMP(3),
        total_precipitation FLOAT
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/postgres',
        'table-name' = 'weather_sink_table',
        'username' = 'flink',
        'password' = 'postgres',
        'driver' = 'org.postgresql.Driver',
        'sink.buffer-flush.max-rows' = '1000',
        'sink.buffer-flush.interval' = '1s'
    )
    """
)

# Process data by unnesting the 'minutely' array and casting dt to TIMESTAMP
table_env.execute_sql(
    """
    INSERT INTO weather_sink
    SELECT
        TO_TIMESTAMP(FROM_UNIXTIME(f.dt), 'yyyy-MM-dd HH:mm:ss') AS dt,
        f.precipitation
    FROM weather_source,
    UNNEST(weather_source.minutely) AS f (dt, precipitation)
    """
)

table_env.execute_sql(
    """
    INSERT INTO weather_hourly
    SELECT
        TUMBLE_START(dt, INTERVAL '1' HOUR) AS event_hour,
        SUM(precipitation) AS total_precipitation
    FROM weather_sink
    GROUP BY TUMBLE(dt, INTERVAL '1' HOUR)

    """
)

# Print a message to indicate job submission
print("Start processing")
