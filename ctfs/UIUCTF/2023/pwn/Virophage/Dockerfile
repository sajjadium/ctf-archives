FROM ubuntu:focal

RUN apt-get update
RUN apt-get install -y xinetd
RUN apt-get clean
RUN useradd -m virus

ADD share/virus /home/virus/virus
ADD share/flag /flag
ADD share/getflag /getflag
ADD share/run.sh /home/virus/run.sh
ADD xinetd /etc/xinetd.d/virus

RUN chown -R virus:virus /home/virus/
RUN chown root:root /getflag
RUN chown root:root /flag
RUN chmod 400 /flag
RUN chmod 4755 /getflag

USER virus
WORKDIR /home/virus/

CMD ["/usr/sbin/xinetd", "-dontfork"]
