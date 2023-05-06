FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update &&\
    apt-get install -y --no-install-recommends wget unzip gcc make libc6-dev gnutls-dev uuid

RUN mkdir -p /server/data/ &&\
    echo "hello from LightFTP" >> /server/data/hello.txt &&\
    cd /server &&\
    wget --no-check-certificate https://codeload.github.com/hfiref0x/LightFTP/zip/refs/tags/v2.2 -O LightFTP-2.2.zip &&\
    unzip LightFTP-2.2.zip &&\
    cd LightFTP-2.2/Source/Release &&\
    make &&\
    cp -a ./fftp /server/ &&\
    cd /server &&\
    rm -rf LightFTP-2.2 LightFTP-2.2.zip

COPY ./flag /flag
COPY ./fftp.conf /server/fftp.conf

RUN mv /flag /flag.`uuid` &&\
    useradd -M -d /server/ -U ftp

WORKDIR /server

EXPOSE 2121

CMD ["runuser", "-u", "ftp", "-g", "ftp", "/server/fftp", "/server/fftp.conf"]
