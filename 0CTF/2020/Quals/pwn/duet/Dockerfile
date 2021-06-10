FROM ubuntu:19.04
ARG USER=ctf
COPY --chown=root:10000 duet flag /
RUN groupadd -g 10000 $USER && useradd -N -u 10000 -g 10000 $USER && chmod 750 /duet && chmod 440 /flag
USER 10000:10000
CMD ["/usr/bin/timeout", "-s9", "300", "/duet"]
