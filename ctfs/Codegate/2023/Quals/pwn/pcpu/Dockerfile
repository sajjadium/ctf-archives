FROM ubuntu:22.04@sha256:dfd64a3b4296d8c9b62aa3309984f8620b98d87e47492599ee20739e8eb54fbf

RUN apt update
RUN apt install -y xinetd python3 python3-pip
RUN python3 -m pip install pwntools

RUN useradd ctf

RUN mkdir /home/ctf
ADD app /home/ctf/app
ADD run.sh /home/ctf/run.sh
ADD precheck.py /home/ctf/precheck.py

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/app
RUN chmod +x /home/ctf/run.sh

ADD xinetd /etc/xinetd.d/
EXPOSE 1234

CMD ["/usr/sbin/xinetd","-dontfork"]