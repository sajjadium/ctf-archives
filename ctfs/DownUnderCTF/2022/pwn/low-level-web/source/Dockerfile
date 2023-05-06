FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y nodejs npm libnode-dev \
  && rm -rf /var/lib/apt/lists/*
RUN npm install -g yarn

RUN groupadd -g 1001 -r ctf && useradd -u 1001 --no-log-init -r -g ctf ctf
WORKDIR /app

COPY ./package*.json ./
COPY ./yarn.lock ./
COPY ./binding.gyp ./
COPY ./build ./build
COPY ./index.js ./
COPY ./public ./public
COPY ./start.sh ./start.sh

RUN ["yarn", "install", "--ignore-scripts"]

USER ctf
ENTRYPOINT ["/app/start.sh"]
