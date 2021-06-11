FROM ubuntu:20.04
ENV USER sauerbraten
RUN useradd $USER

RUN apt-get update
RUN apt-get install -y gdb

COPY flag.txt /home/$USER/flag.txt
COPY flag2.txt /home/$USER/flag2.txt

COPY sauerbraten-code/src/sauer_server /home/$USER/
COPY sauerbraten-code/server-init.cfg /home/$USER/

RUN chmod +x /home/$USER/sauer_server

RUN chown -R root:$USER /home/$USER
RUN chmod -R 555 /home/$USER

EXPOSE 28785

WORKDIR /home/$USER/
USER $USER

ENTRYPOINT ["timeout", "300", "/home/sauerbraten/sauer_server"]