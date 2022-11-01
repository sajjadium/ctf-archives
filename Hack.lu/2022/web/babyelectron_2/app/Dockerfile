FROM node:slim as builder

RUN apt update && \
    apt install -y gcc 

WORKDIR /build
ADD printflag.c .
RUN gcc -o printflag -static printflag.c 

FROM node:slim

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Berlin

ENV DISPLAY :99

ENV BOT=1

RUN apt update && \
    apt install -y curl && \
    apt install -y --no-install-recommends xvfb && \
    apt install -y --no-install-recommends xauth && \
    apt install -y libnss3-dev && \
    apt install -y libgbm-dev && \
    apt install -y libasound2-dev && \
    apt install -y --no-install-recommends xfce4 && \
    apt install -y --no-install-recommends xdg-utils && \
    apt install -y ncat

COPY --from=builder --chown=root:root /build/printflag /printflag

RUN chmod -rw /printflag && \
    chmod +x /printflag

COPY package.json /app/
COPY ./src/ /app/src/

WORKDIR /app
RUN npm install

RUN chown -R node:node /app/

COPY run.sh /app/

USER node
COPY flag.txt /flag

ENTRYPOINT [ "bash", "./run.sh" ]

