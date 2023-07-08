FROM node:lts-slim

ENV NODE_ENV=production

RUN apt-get update \
    && apt-get install -y wget gnupg \
	&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list\
    && apt-get update && apt-get -y install google-chrome-stable

WORKDIR /app

COPY src/package.json src/package-lock.json ./

RUN PUPPETEER_SKIP_DOWNLOAD=true npm install . --omit-dev

COPY src/ .

ENV FLAG=dummy{dummy}
ENV APP_HOST="hex2dec-web.chal.crewc.tf"
ENV APP_PORT=8084
ENV REPORT_DURATION=60

CMD mount -t tmpfs none /tmp && \
    mkdir /tmp/chrome-userdata && chmod o+rwx /tmp/chrome-userdata && \
    node server.js

