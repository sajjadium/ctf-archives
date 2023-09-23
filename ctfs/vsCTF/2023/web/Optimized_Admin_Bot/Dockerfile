FROM node:20

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN chown root:root flag.txt && chmod 400 flag.txt
RUN gcc -o readflag readflag.c
RUN chmod u+s readflag

RUN chown -R node:node /app
USER node

EXPOSE 3000

CMD [ "node", "index.js" ]