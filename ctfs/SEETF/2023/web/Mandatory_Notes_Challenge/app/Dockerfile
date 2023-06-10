FROM node:18-bullseye-slim

RUN apt-get update && \
apt-get install -y dumb-init && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production

RUN addgroup mnc && \
adduser --disabled-password --gecos "" --ingroup mnc mnc

WORKDIR /home/mnc/app
RUN chown -R mnc:mnc .

COPY ./static ./static
COPY main.js package.json index.html ./

RUN npm install

USER mnc

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "./main.js"]
