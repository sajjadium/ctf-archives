FROM ubuntu:22.04 as chroot

RUN apt-get update -y
RUN apt-get install -y vim

RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag.txt /
COPY entry.sh /home/user/
COPY vimrc /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

# This is mostly boring kctf and nsjail setup. The important part to pay
# attention to is the "pty,sane" line.
CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/entry.sh",pty,sane
