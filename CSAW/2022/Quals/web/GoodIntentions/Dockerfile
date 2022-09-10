FROM python:3.7-alpine

# Install packages
RUN apk add --update --no-cache supervisor python3-dev

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
COPY requirements.txt /requirements.txt
RUN python -m pip install -r requirements.txt

# Add user
RUN adduser -D -u 1000 -g 1000 -s /bin/sh www

# Copy flag
COPY flag.txt /flag.txt

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY server .
RUN chown -R www:www .

# Setup supervisor
COPY supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

