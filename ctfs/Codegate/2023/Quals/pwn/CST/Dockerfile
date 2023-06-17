FROM ubuntu:22.04@sha256:dfd64a3b4296d8c9b62aa3309984f8620b98d87e47492599ee20739e8eb54fbf

RUN apt update
RUN apt install -y xinetd python3 llvm

RUN useradd ctf

RUN mkdir /home/ctf
ADD cst /home/ctf/cst
ADD run.sh /home/ctf/run.sh
ADD wrapper.py /home/ctf/wrapper.py
ADD flag /flag

RUN chmod 460 /home/ctf/*
RUN chmod 460 /flag
RUN chown ctf:root /home/ctf/*
RUN chown ctf:root /flag
RUN chmod +x /home/ctf/cst
RUN chmod +x /home/ctf/run.sh

ADD xinetd /etc/xinetd.d/
EXPOSE 1234

CMD ["/usr/sbin/xinetd","-dontfork"]