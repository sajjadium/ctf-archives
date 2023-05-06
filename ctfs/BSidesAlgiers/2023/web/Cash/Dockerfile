FROM python:3.10

RUN apt update -y

RUN apt install -y redis-server

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

# Expose port 5000 for the Flask app
EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Copy the current directory contents into the container at /app
COPY . /app

ENTRYPOINT ["/entrypoint.sh"]
