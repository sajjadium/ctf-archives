# Use the official Python image as a base image
FROM python:3.9

# Install dependencies for Nginx
RUN apt-get update && \
    apt-get install -y nginx wget

RUN groupadd swuser -g 1433 && \
    useradd -u 1433 -g swuser -s /sbin/nologin -c "Docker image user" swuser

RUN mkdir /home/swuser && \
    chown swuser:swuser /home/swuser

# Set the working directory
WORKDIR /app

# Copy the Nginx configuration file
COPY app/nginx.conf /etc/nginx/sites-available/default

# Copy the application code
COPY app/ /app


COPY app/requirements.txt .
RUN pip install -r requirements.txt

RUN chown -R swuser:swuser /app

USER swuser

RUN wget https://p4ctf2023.fra1.digitaloceanspaces.com/geotask_priv/cf8e51e40bc7a1ba30e8eaa90872baff/2023-04-17-geoguessr-20.pth -O /app/geotask/2023-04-17-geoguessr-20.pth

# Expose the ports (80 for Nginx, 8000 for Flask)
EXPOSE 8000


# Start Nginx and the Flask application
USER root
CMD ["sh", "-c", "nginx && gunicorn --workers 6 --user 1433 --bind unix:/tmp/gunicorn.sock app:app"]

