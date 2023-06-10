FROM node:18-bullseye-slim

RUN apt-get update && \
apt-get install -y dumb-init && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production

RUN addgroup ezxxe && \
adduser --disabled-password --gecos "" --ingroup ezxxe ezxxe

WORKDIR /home/ezxxe/app
RUN chown -R ezxxe:ezxxe .

COPY ./static ./static
COPY main.js package.json pigeons.json ./

RUN npm install

USER ezxxe

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "./main.js"]
