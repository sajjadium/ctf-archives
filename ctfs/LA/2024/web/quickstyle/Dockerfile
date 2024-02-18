FROM node:19-bullseye-slim

WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm ci

COPY server.js note.js note.html /app/

ENV PORT=3000
CMD ["node", "/app/server.js"]
