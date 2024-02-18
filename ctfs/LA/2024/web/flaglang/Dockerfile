FROM node:19-bullseye-slim

WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm ci

COPY src/ /app/src/

CMD ["node", "/app/src/app.js"]
