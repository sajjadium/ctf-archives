# ret2winrars
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
  xinetd \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /challenge
RUN useradd -M -d /challenge ctf
WORKDIR /challenge

COPY ctf.xinetd /etc/xinetd.d/ctf
COPY . /challenge/

RUN chown -R ctf:ctf /challenge && chmod -R 770 /challenge
RUN chown -R root:ctf /challenge && \
  chmod -R 750 /challenge

CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 1337
