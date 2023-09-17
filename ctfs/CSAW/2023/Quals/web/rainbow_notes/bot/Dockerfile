FROM node:20-alpine

RUN apk update && apk upgrade
RUN apk add chromium 

RUN mkdir /app
WORKDIR /app
COPY package.json yarn.lock /app/
RUN PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true yarn
# create user `bot`
RUN adduser -D -u 1001 bot && \
    mkdir -p /home/bot && \
    chown -R bot:bot /home/bot

COPY . .
USER bot
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
ENTRYPOINT ["node", "app.js"]
