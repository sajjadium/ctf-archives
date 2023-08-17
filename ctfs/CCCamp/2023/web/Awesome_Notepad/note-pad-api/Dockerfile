FROM node:12.11.0-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn --production --no-progress --frozen-lockfile  install

ADD . /app/

EXPOSE 4000
CMD [ "node", "index.js" ]