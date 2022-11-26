FROM node:16
EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install socat coreutils

COPY chall/ /app

RUN chmod 555 /app/app.js && \
    chmod 444 /app/flag.txt

RUN useradd -ms /bin/sh app
USER app

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"node /app/app.js"
