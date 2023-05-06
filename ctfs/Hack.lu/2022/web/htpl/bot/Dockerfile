FROM node:17-alpine

RUN apk update && apk upgrade
RUN apk add chromium 
WORKDIR /home/node
ENV CHROME_BIN=/usr/bin/chromium-browser
COPY package.json ./
RUN yarn 
COPY index.ts tsconfig.json ./
EXPOSE 4000
CMD yarn start
