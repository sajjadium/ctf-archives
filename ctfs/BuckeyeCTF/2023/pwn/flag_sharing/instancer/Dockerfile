FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y docker.io python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/ctf/instancer
WORKDIR /home/ctf/instancer/

# venv for POW
RUN python3 -m venv venv
RUN bash -c "source venv/bin/activate && pip3 install ecdsa requests proxy-protocol"

COPY ./ /home/ctf/instancer/

EXPOSE 9000
CMD ["./setup.sh"]
