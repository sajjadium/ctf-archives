# see docker-compose.yml

FROM node:current-bullseye
ENV NODE_ENV=production
WORKDIR /app

COPY package.json package-lock.json app.js index.html /app/
COPY flag.txt readflag /
RUN npm install

RUN mkdir views
RUN chown node:node views

RUN chown root:root /flag.txt && chmod 400 /flag.txt
RUN chown root:root /readflag && chmod 4555 /readflag

EXPOSE 3000

USER node
CMD node app.js
