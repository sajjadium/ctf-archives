FROM ubuntu:disco-20200114
MAINTAINER Lys

#RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
#    apt-get update && \
#    DEBIAN_FRONTEND=noninteractive apt-get install -qy xinetd
RUN useradd -m hoc
RUN chown -R root:root /home/hoc
RUN chmod -R 755 /home/hoc

USER hoc
CMD ["/home/hoc/run.sh"]
