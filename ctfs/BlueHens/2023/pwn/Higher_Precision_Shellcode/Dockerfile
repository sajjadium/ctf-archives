FROM ubuntu@sha256:c9cf959fd83770dfdefd8fb42cfef0761432af36a764c077aed54bbc5bb25368
# RUN /usr/sbin/useradd --no-create-home -u 1000 user

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install socat libgcc-12-dev --fix-missing && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /home/ctf
RUN groupadd ctf && useradd -d /home/ctf -g ctf ctf

COPY higher_precision_shell /home/ctf/higher_precision_shell
COPY flag.txt /home/ctf/flag.txt
RUN chmod 444 /home/ctf/flag.txt


EXPOSE 1337/tcp

WORKDIR /home/ctf

ENTRYPOINT socat -dd -T180 TCP4-LISTEN:1337,fork,reuseaddr EXEC:"timeout -k 5 180 ./higher_precision_shell",su=ctf,pty,stderr,setsid,sigint,sane,rawer,iexten=0
