FROM node:18-slim

WORKDIR /usr/src/app

COPY ./src/package*.json ./

RUN npm install --production

COPY ./src .

EXPOSE 3000

CMD [ "node", "app.js" ]