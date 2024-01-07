FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m pip install ecdsa
RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY chal.py /home/user/
COPY flag /home/user/

CMD /usr/bin/python3 /home/user/chal.py
