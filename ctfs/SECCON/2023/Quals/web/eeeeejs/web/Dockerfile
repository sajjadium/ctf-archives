FROM node:20.6.0-slim
WORKDIR /app

COPY ["package.json", "package-lock.json", "./"]
RUN npm install
COPY . .
RUN npm run bundle

USER 404:404
ENV NODE_ENV=production
CMD ["node", "index.js"]
