FROM nsjailcontainer

ADD server.py session.py run_jail.sh flag.txt /opt/app/
ADD jails /opt/app/jails
ADD jailyard/ /opt/jailyard

RUN apt-get update && \
apt-get install -y \
    lib32z1 \
    gcc-multilib \
    uidmap \
    python3 \
    python3-pip && \
rm -rf /var/lib/apt/lists/* && \
#
pip3 install angr && \
#
# Create jailed user
useradd -m inmate && \
#
# Set up nsjail chroot
mkdir /chroot/ && \
chown root:inmate /chroot && \
chmod 770 /chroot && \
chmod 440 /opt/app/flag.txt && \
chmod +x /opt/app/run_jail.sh && \
chown root:inmate /opt/jailyard && \
chmod +x /opt/jailyard/compile.sh && \
#
mkdir /opt/transfer && \
chown root:inmate /opt/transfer && \
chmod 770 /opt/transfer

WORKDIR /opt/app

CMD ["/usr/bin/python3", "/opt/app/server.py"]
