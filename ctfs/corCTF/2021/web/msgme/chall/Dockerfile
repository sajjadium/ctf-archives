FROM node:14-alpine

RUN mkdir -p /app

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

USER node

CMD ["node", "index.js"]