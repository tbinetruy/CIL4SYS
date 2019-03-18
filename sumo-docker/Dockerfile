FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install sumo dependencies
RUN apt update
RUN apt -y install sumo sumo-tools sumo-doc python-pip

# Make port 80 available to the world outside this container
EXPOSE 80

# Install pip deps
RUN pip install -r /app/requirements.txt