########################################################################
FROM debian:buster AS builder
MAINTAINER iwamura

ARG PIN_URL
ENV PIN_ROOT /opt/pin

RUN apt-get update &&\
  apt-get --no-install-recommends -y install curl ca-certificates make g++ systemd &&\
  mkdir -p /opt/musl

# install musl libc
COPY musl/musl_*.deb /opt/musl/
RUN dpkg -i /opt/musl/musl_*.deb

# install Intel Pin and fix permissions
RUN cd /opt &&\
    curl -SL $PIN_URL | tar xz -C /opt --no-same-owner &&\
    mv pin-* pin &&\
    find pin -perm -400 -not -perm -044| xargs chmod a+r &&\
    find pin -perm -100 -not -perm -011| xargs chmod a+x

# install pincette server
COPY src/ /opt/src/
RUN cd /opt/src &&\
    make clean &&\
    make &&\
    make install

########################################################################
FROM builder AS devl

ARG PINCETTE_UID

RUN apt-get update &&\
    apt-get --no-install-recommends -y install \
        xinetd prelink python3 \
        sudo vim procps net-tools netcat gdb &&\
    useradd -m -u ${PINCETTE_UID} pincette &&\
    echo 'pincette ALL=(ALL:ALL) NOPASSWD: ALL' > /etc/sudoers.d/pincette

USER pincette
WORKDIR /opt/src.latest
CMD ["/usr/bin/sudo", "/usr/sbin/xinetd", "-dontfork"]

########################################################################
FROM debian:buster AS prod

ARG PINCETTE_UID

RUN mkdir -p /opt/musl
COPY --from=builder /opt/musl/musl_*.deb /opt/musl/
COPY --from=builder /opt/pin/ /opt/pin/
COPY --from=builder /opt/pincette/ /opt/pincette/
COPY --from=builder /etc/xinetd.d/pincette_server_conf /etc/xinetd.d/
RUN dpkg -i /opt/musl/musl_*.deb &&\
    apt-mark hold musl &&\
    apt-get update &&\
    apt-get --no-install-recommends -y install xinetd prelink python3 &&\
    useradd -u ${PINCETTE_UID} pincette

WORKDIR /root
CMD ["/usr/sbin/xinetd", "-dontfork"]
