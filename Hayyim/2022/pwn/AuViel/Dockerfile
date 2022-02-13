FROM ubuntu:20.04
MAINTAINER JSec

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezon

RUN groupadd -r auviel && useradd -r -g auviel auviel
RUN apt-get update
RUN apt-get install xinetd python3 -y
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

# db update 
RUN apt-get install clamav -y
RUN freshclam
RUN cp -r /var/lib/clamav /usr/local/share/clamav

COPY ./xinetd /etc/xinetd.d/auviel

WORKDIR /home/auviel/
COPY ./share/ ./
RUN chown root:auviel ./ -R
RUN chmod 550 ./clamscan
RUN chmod 550 ./wrapper.py
RUN chmod 550 ./run.sh

CMD ["/usr/sbin/xinetd","-dontfork"]
