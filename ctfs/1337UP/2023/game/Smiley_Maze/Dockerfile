FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y xauth && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

RUN touch ~/.Xauthority

COPY smileymaze .

CMD ["./smileymaze"]
