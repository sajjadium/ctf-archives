FROM node:14-buster-slim

WORKDIR /app
COPY package*.json ./

RUN npm i
COPY . .

ENV NODE_ENV production
RUN chown node:node photobucket
USER node
EXPOSE 3000

CMD ["node", "/app/index.js"]
