FROM ubuntu:bionic

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get update --fix-missing && apt-get -y upgrade && apt-get install -y xinetd python-pip

# install unicorn
RUN pip install unicorn

# Create ctf-user
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir /home/ctf

# Configuration files/scripts
ADD config/ctf.xinetd /etc/xinetd.d/ctf
ADD config/run_challenge.sh /home/ctf/run_challenge.sh

# Challenge files
ADD challenge/flag.txt /flag.txt
ADD challenge/userland /home/ctf/userland
ADD challenge/kernel /home/ctf/kernel
ADD challenge/main /home/ctf/main
ADD challenge/libunicorn.so.1 /usr/lib/libunicorn.so.1

# Set some proper permissions
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/main
RUN chmod 750 /home/ctf/run_challenge.sh
RUN chmod 444 /flag.txt

WORKDIR /home/ctf/
EXPOSE 1337

CMD service xinetd restart && /bin/sleep infinity