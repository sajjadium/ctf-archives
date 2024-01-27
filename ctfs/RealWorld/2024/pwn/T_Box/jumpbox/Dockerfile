FROM ubuntu:22.04

RUN apt-get update && apt install openssh-server iproute2 netcat python3 python3-pip iputils-ping -y

RUN pip install pwntools

RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]