# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies for psycopg2 and other libraries
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5001

# Define environment variable to ensure the app is in production mode
ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]