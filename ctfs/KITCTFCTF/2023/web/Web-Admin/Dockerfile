# docker build -t web-admin . && docker run -p 3000:3000 web-admin

FROM node:18-alpine

USER node
RUN mkdir -p /home/node/app
WORKDIR /home/node/app

COPY --chown=node:node package*.json ./

RUN npm ci

COPY --chown=node:node . .

RUN npm run build

CMD [ "node", "dist/main.js" ]
