# Use the official Python image from the Docker Hub
# Note: Don't use slim as we are going to need Pyflink
FROM openjdk:slim
COPY --from=python:3.6 / /

# Set the working directory in the container
WORKDIR /app

# Copy all files in the app directory into the app directory in the container
COPY ./app /app
COPY requirements.txt .

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpython3-dev \
    curl \
    && apt-get clean
# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run the application
CMD ["python", "main.py"]