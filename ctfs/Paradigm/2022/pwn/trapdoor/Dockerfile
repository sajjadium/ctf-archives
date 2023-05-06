FROM gcr.io/paradigmxyz/ctf/eth-base:latest

COPY deploy/ /home/ctf/

RUN true \
    && /root/.foundry/bin/forge script /home/ctf/Empty.sol \
    && true