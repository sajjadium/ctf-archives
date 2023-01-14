# Credits to https://github.com/ImaginaryCTF/ImaginaryCTF-2022-Challenges/tree/master/Web/CyberCook/challenge
FROM node:18.4-buster-slim

RUN apt-get update && \
apt-get install -y chromium dumb-init && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production \
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

RUN addgroup inmate && \
adduser --disabled-password --gecos "" --ingroup inmate inmate

COPY deploy /home/inmate/app
WORKDIR /home/inmate/app

RUN chown -R inmate:inmate .
USER inmate
RUN npm install && \
mkdir -p /home/inmate/Downloads

VOLUME /tmp

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD node /home/inmate/app/main.js