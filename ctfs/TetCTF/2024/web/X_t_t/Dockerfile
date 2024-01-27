FROM node:slim

# Install packages
RUN apt update && apt install -y --no-install-recommends supervisor gcc libc-dev \
    libnss3-dev libgbm-dev libasound2-dev python3 python3-pip python3-pip-whl \ 
    xfce4 xdg-utils xvfb curl
# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Add application
COPY challenge .



# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

RUN cd /app/app && npm install

# Expose port the server is reachable on
EXPOSE 80

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

# Setup environment for electron
ENV DEBIAN_FRONTEND noninteractive
ENV DISPLAY :99


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
