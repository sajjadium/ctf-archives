FROM node:18.12.0-slim

ENV NODE_ENV=production

WORKDIR /app

COPY ["package.json", "package-lock.json", "./"]

RUN npm install --omit=dev

COPY . .

USER 404:404

CMD ["node", "index.js"]
