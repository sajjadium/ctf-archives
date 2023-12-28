# use the jail base image
FROM pwn.red/jail
# copy the root files from any Docker image
COPY --from=ubuntu / /srv
# setup the binary to run

ENV JAIL_TMP_SIZE=16M

COPY chall /srv
COPY flag.txt /srv
COPY run.sh /srv
COPY gordon.bin /srv
COPY kitchen.bin /srv
RUN chmod +x /srv/chall
RUN chmod +x /srv/run.sh

RUN mkdir /srv/app && ln -s /run.sh /srv/app/run