FROM pwn.red/jail

COPY --from=ubuntu@sha256:80ef4a44043dec4490506e6cc4289eeda2d106a70148b74b5ae91ee670e9c35d / /srv
COPY ./src/z2h /srv/app/z2h
COPY ./src/wrapper.sh /srv/app/run
COPY ./src/flag.txt /srv/app/flag.txt
RUN chmod 555 /srv/app/z2h
RUN chmod 555 /srv/app/run
RUN chmod 444 /srv/app/flag.txt

ENV JAIL_MEM=10M JAIL_TIME=10
