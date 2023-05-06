dpkg-reconfigure openssh-server
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

#useradd -ms /bin/bash ubuntu

#PASSWORD=lemonthink
echo "ubuntu:$PASSWORD" | chpasswd
/usr/sbin/sshd
cd /dist
while true; do  /dist/circus; done
