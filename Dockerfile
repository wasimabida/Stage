# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the working directory
COPY . .

# Install the project dependencies
RUN pip install -r requirements.txt

# Command to run the main.py script
CMD ["python", "main.py"]
