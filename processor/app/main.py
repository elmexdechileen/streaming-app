from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import TimeCharacteristic
from pyflink.datastream import window  # Correct import
from pyflink.datastream.functions import AggregateFunction
from pyflink.common import Types
from pyflink.common.time import Time
from datetime import datetime
from pyflink.datastream.connectors import CassandraSink


def process_weather_data(message):
    data = json.loads(message)
    lat = data["lat"]
    lon = data["lon"]
    minutely_data = data["minutely"]

    for entry in minutely_data:
        dt = entry["dt"]
        precipitation = entry["precipitation"]
        print(f"Timestamp: {dt}, Precipitation: {precipitation}")


class PrecipitationAggregator(AggregateFunction):
    def create_accumulator(self):
        return 0.0

    def add(self, value, accumulator):
        return accumulator + value

    def get_result(self, accumulator):
        return accumulator

    def merge(self, a, b):
        return a + b


def extract_precipitation(message):
    data = json.loads(message)
    minutely_data = data["minutely"]
    results = []
    for entry in minutely_data:
        dt = entry["dt"]
        precipitation = entry["precipitation"]
        results.append((dt, precipitation))
    return results


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    # Example Kafka Consumer configuration
    kafka_consumer = FlinkKafkaConsumer(
        topics="weather",
        deserialization_schema=SimpleStringSchema(),
        properties={"bootstrap.servers": "kafka:29092", "group.id": "weather_group"},
    )

    # Data stream from Kafka
    weather_stream = env.add_source(kafka_consumer)

    # Extract precipitation data and map it
    weather_stream = weather_stream.flat_map(
        lambda message: extract_precipitation(message),
        output_type=Types.TUPLE([Types.LONG(), Types.FLOAT()]),
    )

    # Watermark strategy: Using a simple timestamp extractor for Flink 1.16
    weather_stream = weather_stream.assign_timestamps_and_watermarks(
        WatermarkStrategy.for_monotonous_timestamps().with_timestamp_assigner(  # Simple watermark strategy
            lambda x, _: x[0]
        )  # Using the timestamp from the tuple (dt)
    )

    # Key by hourly timestamp and apply tumbling window
    weather_hourly = (
        weather_stream.key_by(
            lambda x: datetime.fromtimestamp(x[0]).strftime("%Y-%m-%d %H:00:00")
        )
        .window(
            window.TumblingEventTimeWindows.of(Time.hours(1))
        )  # Correct window import for 1.16
        .aggregate(PrecipitationAggregator(), output_type=Types.FLOAT())
    )

    # Format the result for Cassandra
    weather_hourly = weather_hourly.map(
        lambda x: (datetime.fromtimestamp(x[0]).strftime("%Y-%m-%d %H:00:00"), x[1])
    )

    # Set up Cassandra Sink
    cassandra_sink = CassandraSink.add_sink(weather_hourly)
    cassandra_sink.set_query(
        "INSERT INTO weather_data.hourly (timestamp, precipitation) VALUES (?, ?);"
    )
    cassandra_sink.set_host("cassandra:9042")
    cassandra_sink.build()

    # Execute the Flink job
    env.execute("Weather Data Processing")


if __name__ == "__main__":
    main()
