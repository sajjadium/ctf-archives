FROM node:12-slim

WORKDIR /app

COPY ./app ./

RUN npm install

COPY ./app/package*.json ./
ENV FLAG=wsc{redacted}

EXPOSE 80

CMD [ "npm", "start" ]