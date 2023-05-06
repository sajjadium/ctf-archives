FROM ubuntu:18.04
RUN cp /etc/apt/sources.list /etc/apt/sources.list.backup
RUN rm -f /etc/apt/sources.list
COPY ./sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install qemu-system-x86
RUN apt-get -y install libsdl2-2.0-0
RUN apt-get -y install libnfs11
RUN apt-get -y install libsnappy1v5
COPY ./flag /
RUN chmod 444 /flag
ADD pwn_file.tar.gz /home/
WORKDIR /home/pwn_file
RUN useradd -m pwn
USER pwn
CMD /home/pwn_file/launch.sh
