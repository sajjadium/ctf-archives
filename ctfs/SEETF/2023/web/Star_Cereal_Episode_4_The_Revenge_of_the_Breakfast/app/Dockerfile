FROM node:18-bullseye-slim

RUN apt-get update && \
apt-get install -y dumb-init && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production

RUN addgroup starcereal && \
adduser --disabled-password --gecos "" --ingroup starcereal starcereal

WORKDIR /home/starcereal/app
RUN chown -R starcereal:starcereal .

COPY ./static ./static
COPY main.js package.json index.html ./

RUN npm install

RUN mkdir ./uploads && chown -R  starcereal:starcereal ./uploads

USER starcereal

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "./main.js"]
