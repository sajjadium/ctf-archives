FROM ubuntu

RUN mkdir -p /srv/app/
WORKDIR /srv/app/

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

COPY ./uncurved /srv/app/run
COPY ./libc-2.31.so /srv/app/libc-2.31.so
COPY ./ld-2.31.so /srv/app/ld-2.31.so
COPY ./flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run /srv/app/libc-2.31.so /srv/app/ld-2.31.so
RUN chmod 744 /srv/app/flag.txt

RUN adduser --system --shell /bin/sh ractf
USER ractf

CMD ["socat", "-T120", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/app/run"]