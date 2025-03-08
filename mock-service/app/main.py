"""
This module contains a Flask application that provides a mock weather API service.
The application includes the following endpoint:
- /data/3.0/onecall (GET): Returns mock weather data including latitude, longitude,
    timezone, timezone offset, and minute-by-minute precipitation data.
The mock data is generated using random values to simulate real weather data.
"""

import random
import time
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/data/3.0/onecall", methods=["GET"])
def one_call():
    """
    Mock function to simulate a weather API one call response.

    Returns:
        Response: A Flask JSON response containing mock weather data.
        The response includes:
        - lat (float): Latitude of the location.
        - lon (float): Longitude of the location.
        - timezone (str): Timezone of the location.
        - timezone_offset (int): Offset from UTC in seconds.
        - minutely (list): List of dictionaries containing minute-by-minute precipitation data.
            - dt (int): Unix timestamp of the data point.
            - precipitation (float): Precipitation volume for the minute in mm.
    """

    current_timestamp = int(time.time())
    minutely_data = [
        {
            "dt": current_timestamp + i * 60,
            "precipitation": (
                # Generate random precipitation values with a 30% chance of no precipitation,
                # I don't know if this is accurate but lets not go in to Markov chains
                round(random.gauss(1, 0.5), 2)
                if random.random() < 0.3
                else 0.0
            ),
        }
        for i in range(60)
    ]

    mock_response = {
        "lat": 52.084516,
        "lon": 5.115539,
        "timezone": "Europe/Amsterdam",
        "timezone_offset": 3600,
        "minutely": minutely_data,
    }

    return jsonify(mock_response)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
