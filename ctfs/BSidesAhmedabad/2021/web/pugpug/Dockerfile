FROM node:16-slim

RUN apt update && apt install -y procps

WORKDIR /app
COPY package.json ./
COPY index.js ./
COPY util.js ./
RUN npm install

RUN chown -R node:node /app
USER node

EXPOSE 3000
CMD ["node", "index.js"]
