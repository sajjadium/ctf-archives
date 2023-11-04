FROM asuri/ctf-xinetd

RUN rm -rf /etc/xinetd.d/* && \
  apt-get update && \
  apt-get -y upgrade --option=Dpkg::Options::=--force-confdef

COPY ./ctf.conf /etc/xinetd.d/ctf
COPY ./src /home/user

WORKDIR /home/user

RUN chmod 444 /etc/xinetd.d/ctf
