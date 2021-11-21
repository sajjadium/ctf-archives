FROM ubuntu:21.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd build-essential python python-dev socat

RUN useradd -m ctf
RUN echo 'ctf - nproc 1500' >>/etc/security/limits.conf
COPY ./flag /flag
COPY ./jerry /jerry
COPY ./wrapper.py /wrapper.py
RUN chmod u+x ./wrapper.py
RUN chown ctf:ctf /jerry && chmod 750 /jerry

CMD socat TCP-LISTEN:8888,reuseaddr,fork EXEC:"/wrapper.py"
EXPOSE 8888
