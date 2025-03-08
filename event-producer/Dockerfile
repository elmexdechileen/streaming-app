# Using the official Confluent Kafka image as the base image 
# to make sure we have this producer.
FROM  apache/kafka:3.9.0

# Copy the producer script into the container
USER root
RUN apk update && apk add curl jq

COPY producer.sh /usr/local/bin/producer.sh

# Make the script executable
RUN chmod +x /usr/local/bin/producer.sh

# Start the cron daemon
CMD ["/usr/local/bin/producer.sh"]
