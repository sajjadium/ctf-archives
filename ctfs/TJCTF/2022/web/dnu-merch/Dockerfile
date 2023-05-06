FROM node:14-buster-slim

COPY package.json package-lock.json /app/
WORKDIR /app

ENV ENV=development
RUN npm i

COPY . .

EXPOSE 8080

CMD ["node", "/app/index.js"]
