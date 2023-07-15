FROM node:20-slim

ENV NODE_ENV=production

WORKDIR /app

COPY app/package.json app/package-lock.json /app/
RUN npm install
COPY app/ /app/

CMD [ "node", "index.js" ]