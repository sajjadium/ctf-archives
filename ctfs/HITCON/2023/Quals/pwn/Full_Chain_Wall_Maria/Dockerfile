FROM ubuntu:23.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y xinetd libpixman-1-dev libepoxy-dev libspice-server-dev libfdt-dev libusb-1.0.0-dev libasound-dev libaio-dev libslirp-dev

RUN apt-get clean
RUN useradd -m user

ADD share/flag /home/user/flag
ADD share/qemu-system-x86_64 /home/user/qemu-system-x86_64
ADD share/bios /home/user/bios
ADD share/run.sh /home/user/run.sh
ADD share/bzImage /home/user/bzImage
ADD share/initramfs.cpio.gz /home/user/initramfs.cpio.gz
ADD xinetd /etc/xinetd.d/maria

RUN chown -R user:user /home/user/

USER user
WORKDIR /home/user/

CMD ["/usr/sbin/xinetd", "-dontfork"]
