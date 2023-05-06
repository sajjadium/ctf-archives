FROM ubuntu:20.04
ENV USER babyrarf
RUN useradd $USER

COPY flag.txt /home/$USER/flag.txt
COPY babyrarf /home/$USER/babyrarf

RUN chown -R root:$USER /home/$USER
RUN chmod -R 555 /home/$USER
EXPOSE 1337
RUN apt-get update
RUN apt-get install -y xinetd
COPY $USER.xinetd /etc/xinetd.d/$USER

CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
