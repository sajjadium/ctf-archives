FROM node:alpine
COPY ./src /app
WORKDIR /app
RUN npm ci --only=production

CMD node index.js