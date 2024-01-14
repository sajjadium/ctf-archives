FROM node:20-bullseye-slim

WORKDIR /usr/src/app

ENV FLAG=uoftctf{this_is_a_fake_flag}

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD [ "node", "server.js" ]
