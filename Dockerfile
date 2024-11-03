# Dockerfile for the Python Worker

# Use the official Python image as a base
FROM python:3.10.12

RUN apt-get update && apt-get install -y xclip
# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "agent.py", "dev"]
