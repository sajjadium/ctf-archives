FROM pwn.red/jail
COPY --from=ubuntu:22.04 / /srv
COPY hook.sh /jail/
COPY flag.txt boogie-woogie chroot.sh /srv/app/
COPY run.sh /srv/app/run
ENV JAIL_DEV=null,zero,urandom,ptmx JAIL_PIDS=20 JAIL_TIME=60
