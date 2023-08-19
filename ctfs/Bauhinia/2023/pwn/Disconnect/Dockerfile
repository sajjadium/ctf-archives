FROM ubuntu:22.10

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        tini xinetd \
        python3 sudo\
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home disconnect && mkdir -p disconnect
RUN useradd --no-create-home limiteduser

RUN passwd -d disconnect
RUN echo "disconnect ALL=(limiteduser) NOPASSWD: /sandbox /tmp/*" > /etc/sudoers.d/limiteduser

COPY ./src/setup.py /home/disconnect/setup.py
COPY ./app.xinetd /etc/xinetd.d/app
COPY ./src/flag.txt /

COPY ./src/sandbox /sandbox

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

RUN chmod 555 /sandbox

WORKDIR /home/disconnect
EXPOSE 9999

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]
