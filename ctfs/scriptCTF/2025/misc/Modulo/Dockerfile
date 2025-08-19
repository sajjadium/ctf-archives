FROM python:3.10-alpine3.19

RUN apk update && apk add socat && adduser -D -h /home/chall -s /bin/bash chall
COPY jail.py /home/chall/jail.py


USER chall
ENTRYPOINT ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:\"python /home/chall/jail.py\""]
