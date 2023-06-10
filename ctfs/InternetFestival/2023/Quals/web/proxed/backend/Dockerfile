FROM node:17.6

WORKDIR /app

COPY package*.json ./
RUN npm install

RUN groupadd appgroup && useradd -g appgroup appuser 

COPY ./ ./

USER appuser

CMD ["node", "app.js"]