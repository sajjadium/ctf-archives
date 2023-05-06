# see docker-compose.yml

FROM node:19

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY flag files/* /home/ctf/

USER ctf

CMD sh run.sh