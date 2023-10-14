FROM ubuntu:22.04

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install xinetd libnfs-dev libiscsi-dev libsnappy-dev libssh-dev libpixman-1-dev liblzo2-dev \
    libnuma-dev librbd-dev libcurl4-gnutls-dev libgtk-3-dev libepoxy-dev libbrlapi-dev libxen-dev \
    libvte-2.91-dev libvdeplug-dev libvde-dev libbz2-dev libcapstone-dev libspice-server-dev libfdt-dev \
    libusb-1.0.0-dev libasound-dev libaio-dev libslirp-dev libsndio-dev libusbredirparser-dev libsdl2-2.0-0
    
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD build/pwn.xinetd /etc/xinetd.d/pwn
ADD build/init.sh /etc/init.sh
RUN chmod 700 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
ADD release .
RUN chmod a+x qemu-system-x86_64 run.sh

RUN echo "ISITDTU{XXXXXXXX}" > flag.txt
RUN chmod 440 flag.txt
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

RUN chown -R root:pwn /home/pwn
RUN chmod -R go-w /home/pwn
