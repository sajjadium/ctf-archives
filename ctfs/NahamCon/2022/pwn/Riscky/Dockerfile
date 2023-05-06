FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y \
    && apt-get install -y xinetd qemu-user \
    && apt-get clean -y

# Create challenge user
RUN useradd -u 1000 -d /home/challenge -s /bin/bash challenge
RUN mkdir /home/challenge

# Poor man's pipe to docker logs
RUN ln -sf /proc/1/fd/1 /var/log/challenge.log

# Copy xinetd and other dependencies
COPY challenge.xinetd /etc/xinetd.d/challenge
COPY entrypoint.sh /entrypoint.sh
COPY start.sh /start.sh

RUN chmod 551 entrypoint.sh

# Set up challenge and flag
COPY riscky /
COPY flag.txt /

RUN chmod 444 /flag.txt
RUN chmod 755 /start.sh
RUN chmod 555 /riscky

CMD ["/entrypoint.sh"]

EXPOSE 9999
