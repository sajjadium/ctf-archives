# see docker-compose.yml

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends lighttpd libsqlite3-dev python3 python3-selenium chromium-driver
RUN apt-get install -y strace
RUN rm -rf /var/lib/apt/lists/ /usr/lib/systemd/*

RUN useradd --create-home --shell /bin/bash ctf

COPY proxy /
COPY flag.txt /flag.txt
COPY asmbb-challenge.tar.gz /home/ctf/.
COPY preregister_admin.py /home/ctf/.
COPY run.sh /home/ctf/.
COPY readflag /readflag

RUN cd /home/ctf && tar -xf asmbb-challenge.tar.gz
RUN sed -i '/server.bind/c\server.bind = "0.0.0.0"' /home/ctf/asmbb-challenge/lighttpd.conf
RUN chown root:root /flag.txt && chmod 400 /flag.txt
RUN chown root:root /readflag && chmod 4555 /readflag
RUN chown ctf:ctf -R /home/ctf/asmbb-challenge/
RUN chmod 555 /proxy

EXPOSE 8091

USER ctf

CMD /home/ctf/run.sh

