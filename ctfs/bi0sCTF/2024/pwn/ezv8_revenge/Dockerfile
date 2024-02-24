FROM ubuntu:22.04

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN apt-get -y install python3
RUN apt-get -y install libicu-dev
RUN apt-get -y install libatomic1
RUN apt-get -y install libstdc++6

RUN useradd -m ctf
RUN echo "ctf:ctf" | chpasswd
WORKDIR /home/ctf

ADD d8 /home/ctf
ADD server.py /home/ctf
ADD snapshot_blob.bin /home/ctf
ADD ynetd /home/ctf
ADD run.sh /home/ctf
COPY flag /
COPY catflag /
RUN chown -R root:root /home/ctf
RUN chmod -R 555 /home/ctf

RUN chown 200000:200000 /flag && chmod 400 /flag
RUN chown 200000:ctf /catflag && chmod 755 /catflag && chmod u+s /catflag


USER ctf
EXPOSE 5555
CMD ./ynetd -p 5555 "timeout 30 ./run.sh"
