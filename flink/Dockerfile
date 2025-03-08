# Use the Flink 1.20.1-java17 image as a base
# FROM flink:1.20.1-java17
FROM flink:1.19.2-java17

# Set the URLs for the Kafka connector, Kafka clients JARs, and flink-python JAR
# ENV KAFKA_CONNECTOR_URL https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.4.0-1.20/flink-connector-kafka-3.4.0-1.20.jar
# ENV KAFKA_CLIENTS_URL https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar
# ENV FLINK_PYTHON_URL https://repo1.maven.org/maven2/org/apache/flink/flink-python/1.20.1/flink-python-1.20.1.jar
# ENV FLINK_SQL_CONNECTOR https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.4.0-1.20/flink-sql-connector-kafka-3.4.0-1.20.jar
# ENV FLINK_POSTGRES https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/1.20.1/flink-connector-jdbc-1.20.1.jar
# ENV FLINK_JDBC https://repo1.maven.org/maven2/org/apache/flink/flink-sql-jdbc-driver/1.20.1/flink-sql-jdbc-driver-1.20.1.jar
# ENV POSTGRES_DRIVER https://jdbc.postgresql.org/download/postgresql-42.5.0.jar

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


# Expose Flink's default web UI port (optional)
EXPOSE 8081

# Run Flink as the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
