FROM ubuntu:22.04@sha256:b4b521bfcec90b11d2869e00fe1f2380c21cbfcd799ee35df8bd7ac09e6f63ea
MAINTAINER James

RUN apt-get update && apt-get install libc6 -qy
COPY /share/guardian.conf /etc/ld.so.conf.d/guardian.conf
RUN rm /etc/ld.so.cache && ldconfig -N

CMD ["/bin/bash"]
