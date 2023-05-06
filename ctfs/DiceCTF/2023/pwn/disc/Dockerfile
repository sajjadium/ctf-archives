FROM ubuntu@sha256:c985bc3f77946b8e92c9a3648c6f31751a7dd972e06604785e47303f4ad47c4c as base

FROM pwn.red/jail:0.3.1
COPY --from=base / /srv
COPY disc /srv/app/run
COPY rom.dat /srv/app/
ENV JAIL_MEM=100M JAIL_CPU=500
