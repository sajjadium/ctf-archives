FROM ubuntu:22.04

RUN apt-get update && apt-get -y install xinetd

RUN useradd -M ctf

WORKDIR /ctf

COPY xinetd.conf ./
COPY challenge.sh ./
COPY banner_fail ./
COPY flag.txt ./
COPY chal ./

RUN ln -s /bin/sh /sh

RUN apt-get install uuid-runtime
RUN mv ./flag.txt ./$(uuidgen)

CMD ["xinetd", "-dontfork", "-f", "xinetd.conf"]
