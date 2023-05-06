# docker build . -t panda --network=host
FROM node:16.10-bullseye-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && apt upgrade -y
RUN groupadd -r ctf && useradd -r -g ctf ctf
ADD . /app

WORKDIR /app
RUN chown -R root:ctf /app
RUN npm install

USER ctf
CMD ["node", "server.js"]
