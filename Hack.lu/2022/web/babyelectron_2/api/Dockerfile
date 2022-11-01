FROM node:alpine

COPY ./images/ /app/images/
WORKDIR /app

COPY package.json server.js /app/

RUN npm install

RUN chown -R node:node /app
USER node

CMD ["node", "server.js"]