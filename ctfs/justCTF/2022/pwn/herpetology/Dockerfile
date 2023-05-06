FROM python:3.10

RUN apt-get update && apt-get install -y --no-install-recommends socat && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R

ARG FLAG=justCTF{dummy-flag}
RUN echo $FLAG > /flag.txt

RUN mkdir /task
WORKDIR /task
COPY ./herpetology.py ./

USER jailed
CMD ["socat", "tcp-listen:37259,reuseaddr,fork", "exec:./herpetology.py,nofork"]
