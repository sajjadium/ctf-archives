FROM ubuntu@sha256:c9cf959fd83770dfdefd8fb42cfef0761432af36a764c077aed54bbc5bb25368
# RUN /usr/sbin/useradd --no-create-home -u 1000 user

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && \
	apt-get -y install socat libgcc-12-dev python3 --fix-missing && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /home/ctf
RUN groupadd ctf && useradd -d /home/ctf -g ctf ctf

COPY chall.py /home/ctf/chall.py
COPY flag.txt /home/ctf/flag.txt
RUN chmod 444 /home/ctf/flag.txt


EXPOSE 1337/tcp

WORKDIR /home/ctf

ENTRYPOINT socat -dd -T180 TCP4-LISTEN:1337,fork,reuseaddr EXEC:"timeout -k 5 180 /bin/python3 ./chall.py",su=ctf,pty,stderr,setsid,sigint,sane,rawer,iexten=0
