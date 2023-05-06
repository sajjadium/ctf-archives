FROM node:14-alpine

RUN mkdir -p /app

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

CMD ["node", "index.js"]