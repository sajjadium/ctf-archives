# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get --assume-yes update && apt-get --assume-yes install wget unzip

# Install any needed packages specified in requirements.txt
RUN pip install flask

# Install nuclei
RUN wget "https://github.com/projectdiscovery/nuclei/releases/download/v2.9.15/nuclei_2.9.15_linux_amd64.zip"
RUN unzip nuclei_2.9.15_linux_amd64.zip
RUN rm nuclei_2.9.15_linux_amd64.zip

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
