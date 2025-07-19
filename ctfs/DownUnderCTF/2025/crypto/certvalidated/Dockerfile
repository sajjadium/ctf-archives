FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y wget socat python3-pip swig \
    && rm -r /var/lib/apt/lists/*

RUN pip install endesive==2.18.5

USER 1000
WORKDIR /home/ctf

COPY ./flag.txt /home/ctf/
COPY ./root.crt /home/ctf/
COPY ./certvalidated.py /home/ctf/certvalidated.py

COPY --chmod=755 entrypoint.sh /home/ctf/entrypoint.sh
ENTRYPOINT ["/home/ctf/entrypoint.sh"]
