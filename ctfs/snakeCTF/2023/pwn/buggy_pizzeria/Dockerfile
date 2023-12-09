FROM pwn.red/jail          
COPY --from=ubuntu@sha256:56887c5194fddd8db7e36ced1c16b3569d89f74c801dc8a5adbf48236fb34564 / /srv
COPY pizzeria /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
