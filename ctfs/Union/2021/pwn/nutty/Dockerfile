FROM ubuntu
ENV USER nutty
RUN useradd $USER

COPY initramfs.cpio /home/$USER/initramfs.cpio
COPY bzImage /home/$USER/bzImage
COPY start.sh /home/$USER/start.sh
COPY run.sh /home/$USER/run.sh
COPY pow.py /home/$USER/pow.py
COPY hashcash.py /home/$USER/hashcash.py

RUN chown -R root:$USER /home/$USER
RUN chmod -R 555 /home/$USER
EXPOSE 1337
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata 
RUN apt-get install -y xinetd python2 qemu qemu-system-x86
COPY $USER.xinetd /etc/xinetd.d/$USER

CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
