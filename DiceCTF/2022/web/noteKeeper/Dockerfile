FROM node:current-buster-slim
    
RUN mkdir -p /app

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN chown node:node /app/uploads

USER node

CMD ["node", "index.js"]