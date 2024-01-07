FROM python:3.11.1

RUN /usr/sbin/useradd -u 1000 user

RUN python3 -m pip install flask waitress 
RUN apt-get update
RUN apt-get install -y socat

COPY chal.py /home/user/
COPY run.sh /home/user/
COPY index.html /home/user/

CMD /home/user/run.sh
