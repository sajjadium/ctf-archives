FROM ubuntu:22.04

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install socat
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD . /home/ctf

WORKDIR /home/ctf
RUN echo "potluck{fake_flag}" > flag.txt
RUN chmod 440 flag.txt
RUN chmod 550 myP1G

RUN chown -R root:ctf /home/ctf

USER ctf
CMD socat TCP-L:9999,reuseaddr,fork EXEC:"./myP1G stdout"