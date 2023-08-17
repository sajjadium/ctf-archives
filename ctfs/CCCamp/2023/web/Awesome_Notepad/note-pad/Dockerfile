FROM node:12.11.0-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn  --no-progress --frozen-lockfile install

ADD . /app/

RUN yarn build

USER node
EXPOSE 3000
CMD ["node", "server/server.js"]