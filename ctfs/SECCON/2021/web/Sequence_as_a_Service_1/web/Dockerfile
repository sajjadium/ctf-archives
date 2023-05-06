FROM node:17.0.1-slim
ENV NODE_ENV=production

WORKDIR /app

COPY ["server/package.json", "server/package-lock.json", "./"]

RUN npm install --production

COPY server .
COPY flag.txt /

USER 404:404

CMD ["node", "index.js"]
