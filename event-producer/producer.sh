#!/bin/bash

while true; do
    # URL to fetch data from
    URL="$HOST/data/3.0/onecall?lat=$LAT&lon=$LON&exclude=$EXCLUDE&units=$UNITS&appid=$APPID"

    # Output file
    OUTPUT_FILE="result.json"

    # Fetch data and store in the output file
    curl -s "$URL" -o $OUTPUT_FILE

    # Fetch data and send to Kafka
    jq -rc . $OUTPUT_FILE | /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server "$KAFKA_HOST" --topic $KAFKA_TOPIC

    # Check if the curl command was successful
    if [ $? -eq 0 ]; then
        echo "Data successfully fetched and stored in $OUTPUT_FILE"
    else
        echo "Failed to fetch data from $URL"
    fi

    # Sleep 60 seconds
    sleep 60
done
