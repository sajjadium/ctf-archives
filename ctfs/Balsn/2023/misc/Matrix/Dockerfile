FROM python:3.9-buster
MAINTAINER James

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install xinetd -qy
RUN pip3 install --no-cache-dir numpy torch --index-url https://download.pytorch.org/whl/cpu
RUN useradd -m Matrix

CMD ["/usr/sbin/xinetd", "-dontfork"]
