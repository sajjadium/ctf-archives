FROM node:20-slim

ENV NODE_ENV=production

WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm install
COPY index.js index.html data.json /app/

CMD [ "node", "index.js" ]