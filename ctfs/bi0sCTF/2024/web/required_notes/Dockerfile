FROM node:20.2.0-alpine

RUN apk update && apk upgrade
RUN apk add chromium 

WORKDIR /app
COPY . /app/
RUN mkdir -p /app/notes

RUN PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1 npm install
RUN chmod +x /app/index.js
RUN rm *.json

RUN adduser -D -u 1001 bot &&  chown -R bot:bot /app/notes &&  chown bot:bot /app/settings.proto

USER bot
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
ENTRYPOINT ["node", "index.js"]