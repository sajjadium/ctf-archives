FROM node:latest

LABEL maintainer=Einstrasse

COPY ./server /server
COPY ./flag.txt /flag.txt

EXPOSE 3000

USER root
WORKDIR /server

RUN npm install && npm install --location=global forever
RUN chmod 555 -R /server && chmod 444 /flag.txt


ENTRYPOINT ["su", "node", "-c", "forever app.js"]
