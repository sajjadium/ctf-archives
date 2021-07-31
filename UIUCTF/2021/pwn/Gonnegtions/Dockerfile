FROM ubuntu:20.04
COPY gonnegtions /run/gonnegtions
COPY flag.txt /flag.txt

RUN apt-get -y update
RUN apt-get -y install openssh-server socat libc6-i386

RUN adduser wolfsheim --uid 1337
RUN echo "wolfsheim:gonnegtions" | chpasswd

RUN echo 'ForceCommand "/run/gonnegtions"' >> /etc/ssh/sshd_config
RUN echo 'Port 1339' >> /etc/ssh/sshd_config
RUN mkdir /var/run/sshd

CMD socat TCP-LISTEN:1337,fork,reuseaddr,su=1337 EXEC:"/run/gonnegtions" & socat UDP-LISTEN:1338,fork,reuseaddr,su=1337 EXEC:"/run/gonnegtions" & /usr/sbin/sshd -D
