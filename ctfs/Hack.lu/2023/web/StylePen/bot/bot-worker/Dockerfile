FROM node:18-alpine

RUN apk update && apk upgrade
RUN apk add chromium 

WORKDIR /app/

COPY package.json /app/
RUN npm install

COPY . /app/
ENTRYPOINT ["npm", "start"]