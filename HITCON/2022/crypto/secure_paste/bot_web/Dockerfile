FROM node:18-bullseye-slim

RUN mkdir /app
WORKDIR /app
COPY package.json yarn.lock .
RUN yarn

COPY . .
ENTRYPOINT ["yarn", "start"]
