FROM pwn.red/jail

COPY --from=ubuntu@sha256:f2034e7195f61334e6caff6ecf2e965f92d11e888309065da85ff50c617732b8 / /srv
COPY flipma /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_TIME=60
