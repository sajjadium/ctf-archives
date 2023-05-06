FROM node:18.6.0-bullseye-slim

WORKDIR /app

COPY . .

RUN yarn

EXPOSE 8080

CMD ["node", "/app/index.js"]
