FROM debian:latest as run
FROM pwn.red/jail:0.3.0
COPY --from=run / /srv
RUN mkdir /srv/app
RUN echo "corctf{test_flag}" > /srv/app/flag.txt
COPY harem /srv/app/run
ENV JAIL_MEM=1G JAIL_CPU=500 JAIL_TIME=300 JAIL_POW=5000
