FROM ubuntu@sha256:c1c5a248f628c287d3472d86b0e5c9ca2ef0280475e50b46ad371f566b72e680
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd python3 -y
RUN useradd -m pwn
COPY ./stuff/xinetd.conf /etc/xinetd.d/xinetd
COPY ./stuff/js /home/pwn/js
COPY ./stuff/run.py /home/pwn/run.py
COPY ./stuff/readflag /readflag
COPY ./stuff/libjs/ /libjs/
COPY ./flag.txt /flag.txt
RUN chmod 500 /flag.txt
RUN chmod u+s /readflag
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn 
CMD ["/usr/sbin/xinetd","-dontfork"]
