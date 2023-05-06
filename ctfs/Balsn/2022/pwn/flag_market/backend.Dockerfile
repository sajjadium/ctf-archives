FROM ubuntu:20.04
MAINTAINER how2hack
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get install -y xinetd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip
RUN pip install -U pip flask setuptools gunicorn
RUN useradd -m backend
COPY src/backend/backend.py /backend/
COPY src/backend/run_flag1.sh /backend/
COPY src/backend/run_backend.sh /backend/
COPY ./xinetd-flag1 /etc/xinetd.d/xinetd-flag1
USER backend
CMD /usr/sbin/xinetd -dontfork & /backend/run_backend.sh