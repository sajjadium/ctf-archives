FROM ubuntu:23.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y xinetd qemu-system-x86

RUN apt-get clean
RUN useradd -m user

ADD share/bios /home/user/bios
ADD share/run.sh /home/user/run.sh
ADD share/bzImage /home/user/bzImage
ADD share/initramfs.cpio.gz /home/user/initramfs.cpio.gz
ADD xinetd /etc/xinetd.d/rose

RUN chown -R user:user /home/user/

USER user
WORKDIR /home/user/

CMD ["/usr/sbin/xinetd", "-dontfork"]
