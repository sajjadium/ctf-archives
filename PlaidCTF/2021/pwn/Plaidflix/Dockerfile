# how to use:
# docker build -t plaidflix .
# docker run --rm -p 9001:1337 plaidflix:latest
# nc 127.0.0.1 9001
FROM ubuntu:20.10

RUN apt-get update && apt-get install -y socat

RUN adduser --no-create-home --disabled-password --gecos "" ctf
WORKDIR /home/ctf

COPY --chown=root:ctf bin/plaidflix bin/flag.txt ./
RUN chmod 2750 plaidflix && \
    chmod 0640 flag.txt 

USER ctf
CMD ["socat", "tcp-listen:1337,fork,reuseaddr", "exec:./plaidflix"]

EXPOSE 1337
