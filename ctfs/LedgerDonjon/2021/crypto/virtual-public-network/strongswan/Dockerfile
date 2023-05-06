FROM debian:buster-slim

ENV STRONGSWAN_VERSION="5.6.3"

RUN \
  DEV_PACKAGES="wget make gcc libgmp-dev iptables iproute2" && \
  apt-get -y update && \
  apt-get -y install $DEV_PACKAGES && \
  mkdir /strongswan-build && \
  cd /strongswan-build && \
  wget https://download.strongswan.org/strongswan-$STRONGSWAN_VERSION.tar.gz && \
  tar -xf strongswan-$STRONGSWAN_VERSION.tar.gz && \
  cd strongswan-$STRONGSWAN_VERSION && \
  ./configure --prefix=/usr --sysconfdir=/etc --disable-defaults --enable-gcm --enable-cmd --enable-gmp --enable-ikev2 --enable-charon --enable-socket-default --enable-stroke --enable-updown \
  --enable-aes --enable-hmac --enable-kernel-netlink --enable-nonce --enable-pem --enable-pubkey --enable-random --enable-pkcs1 --enable-pkcs8 --enable-sha1 --enable-sha2 --enable-x509 \
   && \
  make all && make install && \
  apt-get clean && rm -rf /var/lib/apt/lists/

ADD caCert.pem /etc/ipsec.d/cacerts/
ADD serverCert.pem /etc/ipsec.d/certs/
ADD serverKey.pem /etc/ipsec.d/private/

ADD strongswan.conf ipsec.conf ipsec.secrets /etc/
ADD firewall.updown /etc/ipsec.d/

ENTRYPOINT ["/usr/sbin/ipsec"]
CMD ["start", "--nofork"]
