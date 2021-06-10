FROM ubuntu:disco-20200114
RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    dpkg --add-architecture i386 && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy
  
RUN groupadd -r ctf && useradd -r -g ctf ctf

ADD ctf.xinetd /etc/xinetd.d/ctf
ADD ./share/grocery_shop /home/ctf/
ADD ./share/flag /home/ctf/
ADD ./share/run.sh     /home/ctf/

RUN chmod 440 /home/ctf/*
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/run.sh
RUN chmod 750 /home/ctf/grocery_shop
RUN service xinetd restart

CMD ["/usr/sbin/xinetd", "-dontfork"]
