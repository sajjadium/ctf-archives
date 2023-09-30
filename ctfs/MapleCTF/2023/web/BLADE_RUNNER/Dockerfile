FROM node:alpine

WORKDIR /usr/src/app
ENV PORT=6969

# App src
COPY . .

RUN npm install


CMD ["node", "index.js"]