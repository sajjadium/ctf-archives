FROM pwn.red/jail
COPY --from=ubuntu:20.04 / /srv
RUN mkdir /srv/app
ADD chall /srv/app/run
ADD flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run
