# Use the official Python image as a base image
FROM python:3.11-slim

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY receive_event_hubs.py .

# Run the command to start receiving events
CMD ["python", "receive_event_hubs.py"]
