FROM haproxytech/haproxy-debian:2.4

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
       git ca-certificates lsb-release software-properties-common \
       unzip build-essential libssl-dev lua5.3 liblua5.3-dev tcpdump

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY start.sh /

RUN mkdir /tmp/haproxy
WORKDIR /tmp/haproxy

COPY oauth_pubkey.pem .
COPY eth.lua .
COPY reload.sh .
COPY force-reload.sh .
RUN ln -s socket/nginx.socket /var/lib/haproxy/nginx.socket

RUN git clone https://github.com/haproxytech/haproxy-lua-http.git
RUN cp haproxy-lua-http/http.lua .
RUN git clone https://github.com/haproxytech/haproxy-lua-oauth.git
RUN chmod +x haproxy-lua-oauth/install.sh
RUN haproxy-lua-oauth/install.sh luaoauth
RUN rm -r haproxy-lua-http haproxy-lua-oauth

RUN rm -rf /var/lib/apt/lists/*

#COPY http.lua .

VOLUME /tmp
VOLUME /var/log
VOLUME /var/lib/haproxy/
VOLUME /var/run

CMD bash /start.sh
