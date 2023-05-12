FROM node:16.17

WORKDIR /app

COPY ./package*.json /app

RUN npm i

COPY ./ /app/

ENTRYPOINT [ "node", "server.js" ]