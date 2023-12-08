FROM ubuntu
FROM node:18

COPY ./src/ /home/ctf

RUN apt update
RUN apt install -y \
    socat \
    npm

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
WORKDIR /home/ctf
RUN npm install

USER ctf

EXPOSE 3000
ENTRYPOINT socat tcp-l:3000,fork,reuseaddr exec:'node index.mjs' && /bin/bash
