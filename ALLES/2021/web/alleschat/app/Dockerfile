FROM node:slim

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Berlin

ENV DISPLAY :99
ENV XDG_CURRENT_DESKTOP XFCE
ENV BOT 1

RUN apt update && \
    apt install -y curl && \
    apt install -y --no-install-recommends xvfb && \
    apt install -y --no-install-recommends xauth && \
    apt install -y libnss3-dev && \
    apt install -y libgbm-dev && \
    apt install -y libasound2-dev && \
    apt install -y --no-install-recommends xfce4 && \
    apt install -y --no-install-recommends xdg-utils

COPY package.json /app/
COPY ./src/ /app/src/

WORKDIR /app
RUN npm install

RUN chown -R node:node /app/

COPY run.sh readflag flag.txt /app/
RUN chmod +xs readflag && \
    chmod 600 flag.txt

USER node

CMD [ "bash", "./run.sh" ]
