FROM ubuntu

RUN mkdir -p /srv/app
WORKDIR /srv/app

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

COPY ./main /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag.txt

RUN adduser --system --shell /bin/sh ractf
USER ractf

CMD ["socat", "-T120", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/app/run"]