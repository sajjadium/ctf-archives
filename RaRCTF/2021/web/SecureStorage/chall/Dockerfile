FROM node:14-alpine

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app

COPY package.json .

RUN npm install

COPY . .

USER node

CMD ["node", "index.js"]