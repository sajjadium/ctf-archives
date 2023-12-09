FROM node:18-alpine

COPY ./ /app/

RUN apk update && apk upgrade
RUN apk add chromium

WORKDIR /app

RUN npm install express express-rate-limit  puppeteer

EXPOSE 3000

CMD ["node", "server.js"]