FROM ubuntu:22.04
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd python3 -y
RUN useradd -m pwn
COPY ./stuff/xinetd.conf /etc/xinetd.d/xinetd
COPY ./stuff/jerry /home/pwn/
COPY ./stuff/run.py /home/pwn/
COPY ./stuff/readflag /readflag
COPY ./flag.txt /flag.txt
RUN chmod 500 /flag.txt
RUN chmod u+s /readflag
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn 
CMD ["/usr/sbin/xinetd","-dontfork"]