FROM node:17.6

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN groupadd appgroup && useradd -g appgroup appuser 

COPY ./server.js /app/server.js

EXPOSE 4000

USER appuser

CMD node server.js 