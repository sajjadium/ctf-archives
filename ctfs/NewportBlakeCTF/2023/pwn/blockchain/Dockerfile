FROM --platform=linux/amd64 ubuntu:23.04 as deps

FROM --platform=linux/amd64 pwn.red/jail

COPY --from=deps / /srv/
COPY output/libblockchain.so /srv/app/
COPY output/blockchain /srv/app/run
COPY flag.txt /srv/app/

RUN chmod 755 /srv/app/run