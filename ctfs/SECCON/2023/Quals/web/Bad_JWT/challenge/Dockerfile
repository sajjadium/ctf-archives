FROM node:20-slim

ENV NODE_ENV=production

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install . --omit-dev

COPY src/ .

CMD ["node", "index.js"]
