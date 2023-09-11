FROM node:18-alpine AS build
WORKDIR /app
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn install
COPY . /app
RUN node obfuscateActions.js
RUN yarn build
CMD ["yarn", "start"]
