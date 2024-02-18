FROM pwn.red/jail

COPY --from=ubuntu@sha256:f2034e7195f61334e6caff6ecf2e965f92d11e888309065da85ff50c617732b8 / /srv
COPY woogie-boogie /srv/app/woogie-boogie
COPY flag.txt /srv/app/flag.txt
COPY run /srv/app/run
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=20M JAIL_TIME=120 JAIL_PIDS=50
