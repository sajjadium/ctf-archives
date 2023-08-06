FROM ubuntu:22.04@sha256:0bced47fffa3361afa981854fcabcd4577cd43cebbb808cea2b1f33a3dd7f508 AS app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get install qemu-system -y

RUN mkdir /app
WORKDIR /app

COPY bzImage .
COPY initramfs.cpio.gz .
COPY run.sh .
COPY ynetd .

USER nobody

CMD ./ynetd -p 5000 "timeout 70 ./run.sh"

#ENV JAIL_POW=1500
