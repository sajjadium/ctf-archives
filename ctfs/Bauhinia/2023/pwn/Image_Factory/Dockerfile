FROM ubuntu:jammy-20230624
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade \
    && apt-get -y install xinetd git intltool imagemagick \
	libmagickcore-dev pstoedit libpstoedit-dev \
	autopoint build-essential tini python3\
	&& rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home image_factory && mkdir -p /home/image_factory

WORKDIR /home/image_factory
RUN git clone https://github.com/autotrace/autotrace.git \
 && cd autotrace &&./autogen.sh \
 && ./configure --prefix=/usr \
 && make \
 && make install

COPY ./src /home/image_factory/
COPY ./app.xinetd /etc/xinetd.d/app
COPY ./src/flag.txt /
RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;
RUN chmod +x ./chall ./start.sh

EXPOSE 1337
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]