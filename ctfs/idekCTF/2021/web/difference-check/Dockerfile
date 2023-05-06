FROM node:alpine

RUN mkdir /app

WORKDIR /app

ADD . /app

RUN npm install

EXPOSE 1337

ENTRYPOINT ["node", "index.js"]
