FROM node:20.6.0-alpine3.17@sha256:b46062adc42a16400adbc25c766966efee688ddd71ef315a5d333238c817dac8

# Newer alpines don't have mongo so we install from 3.9 :/
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories
RUN apk add --update --no-cache mongodb


RUN mkdir /app
WORKDIR /app
COPY area51 .

RUN npm install

COPY entrypoint.sh /entrypoint.sh
COPY wait_for_mongo.js init_users.js /

EXPOSE 80

RUN adduser \
    --disabled-password \
    --no-create-home \
    "mongo"

# area51 needs home for node log files
RUN adduser \
    --disabled-password \
    "area51"

ENV FLAG="bctf{FaK3_F1aG}"
ENTRYPOINT /entrypoint.sh