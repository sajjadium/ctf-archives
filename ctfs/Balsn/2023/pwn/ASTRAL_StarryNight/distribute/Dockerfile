FROM ubuntu:22.04@sha256:b4b521bfcec90b11d2869e00fe1f2380c21cbfcd799ee35df8bd7ac09e6f63ea
MAINTAINER James

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install xinetd libc6 -qy
RUN useradd -m Astral
RUN groupadd kvm && usermod -aG kvm Astral

CMD /init && /usr/sbin/xinetd -dontfork
