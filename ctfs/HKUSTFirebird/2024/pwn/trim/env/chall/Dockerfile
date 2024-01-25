FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        tini xinetd \
        python3.9 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home lua && mkdir -p /home/lua

COPY ./src /home/lua/
COPY ./app.xinetd /etc/xinetd.d/app

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

WORKDIR /home/lua
RUN chmod +x /home/lua/lua
RUN chmod +x /home/lua/app.py
RUN chmod +x /home/lua/redir.sh

EXPOSE 1337

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]
