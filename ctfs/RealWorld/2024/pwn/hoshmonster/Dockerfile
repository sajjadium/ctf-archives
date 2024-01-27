FROM debian

RUN apt update && apt upgrade -y && apt install -y socat python3-pip
RUN pip install --break-system-packages unicorn filelock fastcrc

WORKDIR             /root
COPY chal.py        /root/

EXPOSE 1337

ENTRYPOINT socat TCP-LISTEN:1337,fork,reuseaddr,bind=0.0.0.0 EXEC:"python3 chal.py",stderr
