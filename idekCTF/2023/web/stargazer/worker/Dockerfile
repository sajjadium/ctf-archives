FROM node:16-buster-slim

RUN apt-get update && \
apt-get install -y chromium dumb-init curl net-tools && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production \
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

RUN addgroup pptr && \
adduser --disabled-password --gecos "" --ingroup pptr pptr

WORKDIR /home/pptr/app
COPY . ./

RUN chown -R pptr:pptr .
USER pptr
RUN npm install

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "./main.js"]