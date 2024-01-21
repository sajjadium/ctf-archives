FROM ubuntu@sha256:e6173d4dc55e76b87c4af8db8821b1feae4146dd47341e4d431118c7dd060a74
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install socat
RUN useradd -m pwn
WORKDIR /home/pwn
COPY ./chall .
COPY ./ld-linux-x86-64.so.2 .
COPY ./libc.so.6 .
RUN echo 'flag{placeholder_for_flag}' > ./flag.txt
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:'timeout 60 su pwn -c ./chall'"]

