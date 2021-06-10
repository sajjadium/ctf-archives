FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y xinetd
RUN apt-get install -y language-pack-en

RUN useradd -m ctf

COPY bin /home/ctf
COPY emojidb.xinetd /etc/xinetd.d/emojidb

RUN chown -R root:root /home/ctf
EXPOSE 9876
CMD ["/home/ctf/start.sh"]
