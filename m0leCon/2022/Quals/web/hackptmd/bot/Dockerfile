FROM node:17.6

RUN apt-get update && apt-get install -y chromium

WORKDIR /app

COPY package*.json ./
RUN npm install

RUN groupadd appgroup && useradd -g appgroup appuser 

COPY ./ ./

EXPOSE 9999

USER appuser

CMD ["node", "server.js"]
