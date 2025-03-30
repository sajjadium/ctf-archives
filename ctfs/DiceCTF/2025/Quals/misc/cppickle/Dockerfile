FROM ubuntu:24.04 AS app
RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m pip install https://download.pytorch.org/whl/cpu-cxx11-abi/torch-2.6.0%2Bcpu.cxx11.abi-cp312-cp312-linux_x86_64.whl numpy --break-system-packages

FROM pwn.red/jail
COPY --from=app / /srv
COPY cppickle.py /srv/app/run
COPY flag.txt /srv/
RUN chmod 444 /srv/flag.txt && mv /srv/flag.txt /srv/flag.`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20`.txt

ENV JAIL_MEM=200M
ENV JAIL_CPU=500
ENV JAIL_PIDS=50
