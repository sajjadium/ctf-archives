# ubuntu 22.04
FROM ubuntu@sha256:bac6081102aae54ba4bcc714695b8f637e42768c7f376f374c428bab043ddc0f
ENV TERM xterm-256color

RUN apt-get update && apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
    wget python3

RUN wget https://github.com/CatalaLang/catala/releases/download/0.9.0/catala-z3-0.9.0-Linux-x86_64 -O /usr/local/bin/catala && \
    chmod +x /usr/local/bin/catala

WORKDIR /ctf

COPY tax.py /ctf
COPY DiceTax.catala_en /ctf

CMD ["python3", "tax.py"]