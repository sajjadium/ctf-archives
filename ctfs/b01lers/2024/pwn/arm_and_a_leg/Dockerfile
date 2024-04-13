# NOTE: Container is running on an aarch64 host
# Memory layout and offsets are the same however addresses will look different

FROM pwn.red/jail

COPY --from=ubuntu@sha256:7185d738658e31c96b3ba0f9deaae1df46a5c405dc82025094a51e5e2072212a / /srv
COPY chal /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=10M JAIL_TIME=120
