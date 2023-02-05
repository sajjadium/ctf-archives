FROM node:19-alpine3.16

WORKDIR /app
COPY package.json ./
COPY public ./public
RUN npm i
COPY app.js .

COPY flag.txt /flag.txt
COPY readflag /readflag
RUN chmod 400 /flag.txt
RUN chmod 6755 /readflag

RUN adduser -D user
USER user

CMD ["/bin/sh", "-c", "while true; do node app.js; done"]