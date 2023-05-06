FROM node:17-alpine

COPY app /app
WORKDIR /app
RUN yarn

ENTRYPOINT ["yarn", "start"]
