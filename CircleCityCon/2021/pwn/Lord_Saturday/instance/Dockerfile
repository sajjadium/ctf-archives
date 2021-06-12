FROM ubuntu:20.04
ENV LC_CTYPE C.UTF-8
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y \
dropbear \
sudo=1.8.31-1ubuntu1 && \
rm -rf /var/lib/apt/lists/* /usr/bin/sudoedit

COPY flag.txt run.sh /

RUN useradd -m --shell /bin/bash ctf && \
chmod 440 /flag.txt

CMD /run.sh
