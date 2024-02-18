FROM pwn.red/jail

COPY --from=ubuntu@sha256:f2034e7195f61334e6caff6ecf2e965f92d11e888309065da85ff50c617732b8 / /srv
COPY calc /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=10M JAIL_TMP_SIZE=1 JAIL_TIME=120 JAIL_CPU=1000 JAIL_POW=6000
