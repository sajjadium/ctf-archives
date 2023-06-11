FROM python:3.9-slim-buster

# Add user 
RUN addgroup --gid 10101 userr && adduser --disabled-password --uid 1010 --gecos "" --ingroup userr userr

# Set the working directory to /userr/app
WORKDIR /home/userr/app

# Copy the current directory contents into the container at /userr/app
COPY app.py init.py requirements.txt /home/userr/app
COPY templates /home/userr/app/templates

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run init.py for setup
RUN python init.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV secret_key <REDACTED>

# Run app.py as userr
USER userr
CMD ["python", "app.py"]
