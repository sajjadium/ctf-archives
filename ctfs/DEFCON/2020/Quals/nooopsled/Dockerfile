from ubuntu:20.04

run DEBIAN_FRONTEND=interactive apt-get update
run DEBIAN_FRONTEND=interactive apt-get install -y qemu-user python3-pip libc6-arm64-cross libc6-riscv64-cross libc6-ppc64-cross xinetd
run pip3 install fuckpy3 forbiddenfruit

COPY service.conf /
COPY banner_fail /
COPY wrapper /
COPY launcher-aarch64 /
COPY launcher-riscv64 /
COPY service.py /
COPY shuffler /

ARG THE_FLAG="OOO{this is a test flag}"
RUN touch /flag && chmod 400 /flag && echo $THE_FLAG > /flag

EXPOSE 5000
CMD ["/usr/sbin/xinetd", "-filelog", "-", "-dontfork", "-f", "/service.conf"]
