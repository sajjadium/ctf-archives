FROM python:3.11-bullseye

WORKDIR /srv/app

ENV DEBIAN_FRONTEND=noninteractive

# Install mysql client dependencies
RUN apt-get update && \
    apt-get -y install python3-dev default-libmysqlclient-dev build-essential && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# App src
COPY ./src .

# Change user
RUN useradd -ms /usr/sbin/nologin app
USER app

EXPOSE 1999

ENTRYPOINT [ "python3", "/srv/app/run.py" ]
