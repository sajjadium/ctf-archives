FROM ubuntu:22.04
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
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./chall"]

