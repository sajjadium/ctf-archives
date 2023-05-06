FROM ubuntu:20.04
ARG USER=ctf
COPY --chown=root:10000 babyheap flag /
RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install musl && groupadd -g 10000 $USER && useradd -N -u 10000 -g 10000 $USER && chmod 750 /babyheap && chmod 440 /flag
USER 10000:10000
CMD ["/usr/bin/timeout", "-s9", "300", "/babyheap"]
