FROM ubuntu:20.04

RUN apt-get update
RUN apt-get update && apt-get install -y build-essential socat libseccomp-dev python3

ARG FLAG
ENV FLAG $FLAG

WORKDIR /
COPY start.sh /start.sh
RUN chmod 755 /start.sh
COPY d8 /d8
RUN chmod 755 /d8
COPY snapshot_blob.bin /snapshot_blob.bin
RUN chmod 755 /snapshot_blob.bin
COPY server.py /server.py
RUN chmod 755 /server.py

# random flag filename
RUN FLAG_FILE=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32); \
    echo $FLAG > $FLAG_FILE; \
    chmod a=r $FLAG_FILE; \
    unset FLAG_FILE

EXPOSE 9000

CMD ["/start.sh"]
