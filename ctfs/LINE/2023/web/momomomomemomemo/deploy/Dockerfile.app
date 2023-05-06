FROM node:16

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

COPY ./src/app ./
RUN npm install

RUN touch data/db.sqlite3 && chown node data/db.sqlite3 && chmod -R 777 data/
USER node

EXPOSE 4040
ENTRYPOINT [ "node", "app.js" ]