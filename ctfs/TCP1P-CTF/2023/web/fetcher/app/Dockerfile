FROM node:alpine

RUN adduser -D ctf
USER ctf
WORKDIR /home/ctf/app

USER root
COPY ./run.sh .
RUN chmod -x run.sh

COPY package.json .
RUN npm install

COPY . .
RUN mv ./flag.txt `cat /proc/sys/kernel/random/uuid`.txt

USER ctf

EXPOSE 8080

CMD [ "/bin/sh", "./run.sh" ]
