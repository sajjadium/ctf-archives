#same dockerfile used to set up all challenges remotely, except changing challenge name
FROM ubuntu:20.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update -y
RUN apt install socat -y

#if libc/ld provided they are hooked with patchelf and coppied as well
COPY walkthrough /home/user/
COPY flag.txt /

USER user

EXPOSE 1337

CMD echo "HI" && socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/home/user/walkthrough"
