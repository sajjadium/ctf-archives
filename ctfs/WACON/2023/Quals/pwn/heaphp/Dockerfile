FROM ubuntu@sha256:ec050c32e4a6085b423d36ecd025c0d3ff00c38ab93a3d71a460ff1c44fa6d77
RUN apt-get update
RUN apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install php8.1-cli -y
RUN apt install xinetd python3 -y
RUN useradd -m pwn
COPY ./stuff/xinetd.conf /etc/xinetd.d/xinetd
COPY ./stuff/run.py /home/pwn/
COPY ./stuff/php.ini /home/pwn/
COPY ./stuff/heaphp.so /home/pwn/heaphp.so
COPY ./stuff/readflag /readflag
COPY ./flag.txt /flag.txt
COPY ./stuff/php8.1 /usr/bin/php8.1
RUN chmod 400 /flag.txt
RUN chmod u+s /readflag
RUN chmod u+x /readflag
RUN chmod +x /usr/bin/php8.1
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn 

CMD ["/usr/sbin/xinetd","-dontfork"]
