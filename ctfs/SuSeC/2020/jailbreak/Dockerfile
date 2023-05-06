FROM ubuntu:18.04

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install socat python3.7
RUN groupadd -r jail && useradd -r -g jail jail

ADD server.py   /home/jail/server.py
ADD libregex.so /home/jail/libregex.so
RUN chmod 550 /home/jail/server.py
RUN chmod 550 /home/jail/libregex.so

RUN chown -R root:jail /home/jail

USER jail
WORKDIR /home/jail
CMD socat TCP-L:9002,reuseaddr,fork EXEC:"python3.7 /home/jail/server.py"
