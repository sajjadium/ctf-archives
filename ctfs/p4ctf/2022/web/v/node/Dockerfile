FROM node

WORKDIR /app

COPY ./package.json ./package.json
RUN npm install

COPY ./index.js ./index.js
COPY ./templates ./templates
CMD ["node", "index.js"]
