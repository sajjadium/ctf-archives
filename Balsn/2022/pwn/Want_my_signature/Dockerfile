FROM ubuntu:20.04
MAINTAINER kevin47
RUN apt-get update
RUN apt-get install python3 python3-pip libsodium-dev -y
RUN pip3 install flask
RUN pip3 install uwsgi
RUN useradd -m want_my_signature
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
COPY ./share /home/want_my_signature
RUN chown -R root:root /home/want_my_signature
RUN chmod -R o-w /home/want_my_signature
RUN chmod 755 /home/want_my_signature
RUN mkdir /tmp/tmp
RUN chmod 733 /tmp/tmp
WORKDIR /home/want_my_signature
CMD ["/usr/local/bin/uwsgi","--gid","want_my_signature","--uid","want_my_signature","--ini","/home/want_my_signature/app.ini"]
