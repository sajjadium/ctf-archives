FROM ubuntu:18.04

# Install prereqs
RUN apt update && apt install -y wget git make gcc python3 python3-pip iproute2

# Setup goahead
WORKDIR /goahead
RUN git clone https://github.com/embedthis/goahead-gpl.git
WORKDIR /goahead/goahead-gpl
RUN git checkout v4.1.4
COPY goahead/patch.diff /tmp/patch.diff
RUN git apply /tmp/patch.diff

## Build/install/setup
RUN make ME_GOAHEAD_SSL=0 ME_COM_SSL=0 ME_GOAHEAD_CLIENT_CACHE_LIFESPAN=10 ME_GOAHEAD_LIMIT_BUFFER=1448 && make install

# Copy in content files
COPY goahead/www/ /var/www/goahead/
COPY goahead/etc/ /etc/goahead/
COPY sensor/ /sensor/
WORKDIR /etc/goahead/
COPY start.sh .
RUN mkdir tmp
RUN mkdir -p /var/www/goahead/data/snapshot
CMD ["./start.sh"]
