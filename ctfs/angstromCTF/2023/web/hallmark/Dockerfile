FROM node:17-bullseye-slim

WORKDIR /app
COPY . .
RUN npm ci

ENV PORT=8080

EXPOSE 8080

CMD ["node", "index.js"]