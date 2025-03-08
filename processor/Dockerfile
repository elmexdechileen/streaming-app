# Use the official Python image from the Docker Hub
# Note: Don't use slim as we are going to need Pyflink
FROM python:3.10

# Install Java
RUN apt-get update && apt-get install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV FLINK_HOME=/opt/flink
ENV FLINK_PLUGINS_DIR=$FLINK_HOME/lib
ENV FLINK_LIB=$FLINK_HOME/lib
ENV CLASSPATH=$FLINK_LIB/*:$CLASSPATH

# Set the working directory in the container
WORKDIR /app

# Copy all files in the app directory into the app directory in the container
COPY ./app /app
COPY requirements.txt .

# Install Kafka connectors
# Create the /opt/flink/lib directory
RUN mkdir -p /opt/flink/lib

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpython3-dev \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    python3-pip \
    && apt-get clean


# Copy all files from the flink-base image's lib directory into the PyFlink container's lib directory
COPY --from=flink:1.19.2-java17 /opt/flink/ /opt/flink/

# Download Kafka connector JARs to /opt/flink/lib
ENV KAFKA_CONNECTOR_URL https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.3.0-1.19/flink-connector-kafka-3.3.0-1.19.jar
ENV KAFKA_CLIENTS_URL https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.0/kafka-clients-3.3.0.jar
ENV FLINK_PYTHON_URL https://repo1.maven.org/maven2/org/apache/flink/flink-python/1.19.2/flink-python-1.19.2.jar
ENV FLINK_SQL_CONNECTOR https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.3.0-1.19/flink-sql-connector-kafka-3.3.0-1.19.jar
ENV FLINK_POSTGRES https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar
ENV FLINK_JDBC https://repo1.maven.org/maven2/org/apache/flink/flink-sql-jdbc-driver/1.19.2/flink-sql-jdbc-driver-1.19.2.jar
ENV POSTGRES_DRIVER https://jdbc.postgresql.org/download/postgresql-42.5.0.jar


ENV FLINK_HOME=/opt/flink
ENV FLINK_LIB=$FLINK_HOME/lib
ENV CLASSPATH=$FLINK_LIB/*:$CLASSPATH


# Download the Kafka connector, Kafka client JARs, and flink-python JARs to the /opt/flink/lib directory
RUN mkdir -p /opt/flink/lib && \
    curl -o /opt/flink/lib/flink-connector-kafka-3.3.0-1.19.jar ${KAFKA_CONNECTOR_URL} && \
    curl -o /opt/flink/lib/kafka-clients-3.3.0.jar ${KAFKA_CLIENTS_URL} && \
    curl -o /opt/flink/lib/flink-python-1.19.2.jar ${FLINK_PYTHON_URL} && \
    curl -o /opt/flink/lib/flink-sql-connector-kafka-3.3.0-1.19.jar ${FLINK_SQL_CONNECTOR} && \
    curl -o /opt/flink/lib/flink-connector-jdbc-3.2.0-1.19.jar ${FLINK_POSTGRES} && \
    curl -o /opt/flink/lib/postgresql-42.5.0.jar ${POSTGRES_DRIVER} && \
    curl -o /opt/flink/lib/flink-sql-jdbc-driver-1.19.2.jar ${FLINK_JDBC}

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the JVM options to open the necessary packages for reflection access
ENV JAVA_TOOL_OPTIONS="--add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED"

# Set the classpath for Flink
ENV FLINK_CLASSPATH=/opt/flink/lib/*:/opt/flink/lib/flink-connector-kafka-3.4.0-1.20.jar:/opt/flink/lib/kafka-clients-3.4.0.jar:flink-sql-connector-kafka-3.4.0-1.20.jar

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run the application
#CMD ["bash", "-c", "python main.py"]
CMD ["bash", "-c", "/opt/flink/bin/flink run -v -m flink:8081 -py main.py -name hourly_weather && tail -f /dev/null"]