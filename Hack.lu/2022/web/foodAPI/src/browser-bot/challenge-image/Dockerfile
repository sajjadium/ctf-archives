FROM debian:stable-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y curl wget unzip netcat\
    # install nodejs
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    # install chrome
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm ./google-chrome-stable_current_amd64.deb \
    && curl -fsSL https://deno.land/x/install/install.sh | sh && mv ~/.deno/bin/deno /usr/local/bin/ 

COPY . /app/
WORKDIR /app/foodAPI
RUN deno cache --import-map import_map.json server.js

WORKDIR /app/
RUN npm install

ENV TIMEOUT_SECS=30
ENTRYPOINT ["bash", "./start.sh"]
