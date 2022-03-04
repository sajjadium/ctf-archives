FROM ubuntu:20.04

RUN apt update -y && apt install -y \
    gcc make

COPY ./src/ /root/

WORKDIR /root
RUN make

CMD ["/bin/bash", "-i"]
