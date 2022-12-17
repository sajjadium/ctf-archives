FROM node:17-alpine
COPY src /src
WORKDIR /src
RUN apk update && apk upgrade
RUN apk add chromium 
RUN npm install express node-fetch express-session body-parser puppeteer dotenv

EXPOSE 3000

CMD ["node", "app.js"]
