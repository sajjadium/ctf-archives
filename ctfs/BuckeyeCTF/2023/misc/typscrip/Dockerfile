FROM node:20-buster-slim as app
WORKDIR /app
COPY package.json package-lock.json app.mjs ./
RUN npm install
CMD node app.mjs