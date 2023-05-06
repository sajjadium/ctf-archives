FROM ubuntu:20.04

# Install prereqs
RUN apt update && apt install -y wget git make gcc python3 python3-pip

# Setup goahead
WORKDIR /goahead
RUN git clone https://github.com/embedthis/goahead.git
WORKDIR /goahead/goahead
RUN git checkout v5.1.4

## Build/install/setup
RUN make ME_GOAHEAD_SSL=0 ME_COM_SSL=0 && make install

# Copy in content files
COPY goahead/etc/ /etc/goahead/
WORKDIR /etc/goahead/
COPY start.sh .
COPY flag.txt /flag
RUN mkdir tmp
CMD ["./start.sh"]
