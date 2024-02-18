FROM ubuntu@sha256:f2034e7195f61334e6caff6ecf2e965f92d11e888309065da85ff50c617732b8 AS app
RUN apt-get update && apt-get install -y \
	qemu-user \
	qemu-user-static \
	binfmt-support \
	&& rm -rf /var/lib/apt/lists/*

FROM pwn.red/jail
COPY --from=app / /srv
COPY arm /srv/app/arm
COPY mips /srv/app/mips
COPY x86 /srv/app/x86
COPY flag.txt /srv/app/flag.txt
COPY polypwn /srv/app/run
RUN chmod 755 /srv/app/run

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENV JAIL_MEM=50M JAIL_PIDS=100 JAIL_CPU=200 JAIL_TIME=60
CMD ["/entrypoint.sh"]
