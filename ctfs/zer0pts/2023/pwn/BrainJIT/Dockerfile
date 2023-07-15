FROM ubuntu:22.04

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install socat python3
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN echo "nek0pts{FAKE_FLAG}" > /flag.txt
RUN chmod 444 /flag.txt
RUN mv /flag.txt /flag-$(md5sum flag.txt | awk '{print $1}').txt

WORKDIR /home/ctf
ADD app.py .
RUN chmod 550 app.py
RUN chown -R root:ctf /home/ctf

USER ctf
CMD socat TCP-L:9999,reuseaddr,fork EXEC:"./app.py"
