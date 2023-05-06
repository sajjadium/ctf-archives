FROM ubuntu:18.04

RUN  apt-get -y update  && \
     apt-get -y install python3  && \
     apt-get -y install python-pyicu && \
     apt-get -y install xinetd

RUN useradd -m ctf

ADD start.sh /root
ADD Release/jsc /home/ctf
ADD Release/lib /home/ctf/lib
ADD server.py /home/ctf
ADD flag /root

ADD run.sh /home/ctf
ADD speedy.xinetd /etc/xinetd.d/speedy
ADD readflag /

RUN chmod +x /root/start.sh && \
    chmod +x /home/ctf/jsc && \
    chmod +x /home/ctf/server.py && \
    chmod +x /home/ctf/lib/libJavaScriptCore.so.1 && \
    chmod +x /home/ctf/run.sh && \
    chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf/   && \
    chmod 4755 /readflag && \
    chmod 400 /root/flag

ENTRYPOINT  /root/start.sh
