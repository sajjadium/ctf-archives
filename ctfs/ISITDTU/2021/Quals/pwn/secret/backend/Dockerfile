FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get update --fix-missing && apt-get -y upgrade

# System deps
RUN apt-get install -y lib32z1 libseccomp-dev xinetd

# Create ctf-user
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir /home/ctf

# Configuration files/scripts
ADD config/ctf.xinetd /etc/xinetd.d/ctf
ADD config/run_xinetd.sh /etc/run_xinetd.sh
ADD config/run_challenge.sh /home/ctf/run_challenge.sh

# Challenge files
ADD challenge/flag /home/ctf/flag
ADD challenge/challenge /home/ctf/challenge

# Set some proper permissions
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/challenge
RUN chmod 750 /home/ctf/run_challenge.sh
RUN chmod 440 /home/ctf/flag
RUN chmod 700 /etc/run_xinetd.sh

RUN service xinetd restart
