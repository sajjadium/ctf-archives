FROM node:17-alpine
COPY src /src
WORKDIR /src
RUN apk update && apk upgrade
RUN apk add chromium 
RUN npm install express puppeteer

EXPOSE 3000

CMD ["node", "app.js"]
