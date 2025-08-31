FROM ubuntu as ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --break-system-packages numba numpy wasmtime scipy

FROM pwn.red/jail
ENV JAIL_TMP_SIZE=16K
env JAIL_PIDS=0
env JAIL_CPU=0
env JAIL_MEM=0

COPY --from=ubuntu / /srv
RUN mkdir /srv/app
COPY flag.txt /srv/app/flag.txt
COPY ctrl.py /srv/app/run
RUN chmod +x /srv/app/run
