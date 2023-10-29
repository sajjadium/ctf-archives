FROM node:16-alpine3.16

ENV LANG="C.UTF-8" PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apk update && \
    apk add --no-cache zlib-dev udev nss ca-certificates chromium && \
    adduser -h /home/bot -D -u 10086 bot && \
    yarn cache clean && \
    rm -rf /tmp/* /etc/apk/* /var/cache/apk/* /usr/share/man

WORKDIR /home/bot

COPY ./*.json .

RUN npm install

COPY . .

USER bot

CMD ["node", "/home/bot/index.js"]
