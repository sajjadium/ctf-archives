FROM ubuntu:latest
MAINTAINER i@shiki7.me 

# Prepare environment and install required packages
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y git libtinfo-dev python3 xz-utils git curl pkg-config xinetd python2.7
RUN mkdir -p /challenge/conf/ /workdir/
RUN curl -sSL https://get.haskellstack.org/ | sh

# Add ctf user
RUN mkdir /home/ctf/ \
  && groupadd -g 1001 ctf \
  && useradd -g ctf -u 1001 -d /home/ctf/ ctf \
  && chown ctf:ctf /home/ctf/

# Add flag
ADD ./flag /flag
RUN chown root:root /flag && chmod 600 /flag
ADD ./flag_reader /flag_reader
RUN chown root:root /flag_reader && chmod 4755 /flag_reader

# Install challenge
ADD ./deploy/server.py /challenge/server.py
ADD ./deploy/run.sh /challenge/run.sh
COPY ./plugin /challenge/plugin
RUN cd /challenge/plugin && stack build

# Setup network
ADD ./problem /etc/xinetd.d/
CMD ["/usr/sbin/xinetd", "-dontfork"]

