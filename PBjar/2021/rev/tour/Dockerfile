FROM ubuntu:20.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update -y
RUN apt install socat -y

COPY tour /home/user/
COPY flag.txt /

USER user

EXPOSE 1337

CMD echo "HI" && socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/home/user/tour"
