FROM python:3.11-slim

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install socat
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf
ADD server.py .
ADD flag.txt .
RUN chmod 550 server.py
RUN chmod 440 flag.txt
RUN chown -R root:ctf /home/ctf

USER ctf
CMD socat TCP-L:9999,fork,reuseaddr EXEC:"python server.py"
