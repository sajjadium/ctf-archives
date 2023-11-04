FROM ubuntu:20.04

RUN apt update && \
        apt -y upgrade && \
        apt install -y python3 build-essential wget

RUN wget https://github.com/ocaml/ocaml/archive/refs/tags/4.12.0.tar.gz
RUN tar zxvf 4.12.0.tar.gz && mv ocaml-4.12.0 ocaml

COPY ./pwn.patch /pwn.patch

WORKDIR /

RUN patch -s -p0 < /pwn.patch
WORKDIR /ocaml
RUN ./configure && make world.opt && make install

RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./env /env
COPY --chown=root:user ./flag /env/flag

WORKDIR /env
RUN chmod 444 flag
RUN mv flag flag-$(md5sum flag | awk '{print $1}')

USER user


ENV PYTHONUNBUFFERED=x
ENV PWN=x
CMD ["./run.py"]
