FROM node:21-alpine

WORKDIR /app

COPY flag.txt /flag.txt
COPY package* .

RUN npm ci

COPY index.js .

CMD node index.js