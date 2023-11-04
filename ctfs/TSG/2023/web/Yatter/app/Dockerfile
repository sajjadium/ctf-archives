FROM node:20-alpine

WORKDIR /app

RUN chown node:node ./

USER node

COPY --chown=node:node package.json package-lock.json ./

RUN npm ci

COPY --chown=node:node . ./

RUN mv flag.txt flag-$(md5sum flag.txt | awk '{ print $1 }').txt

ENTRYPOINT ["node", "server.js"]
