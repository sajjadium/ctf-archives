FROM ubuntu:latest

RUN dpkg --add-architecture i386

RUN apt-get update \
    && apt-get install -y socat libc6-i386 \
    && apt-get install -y libseccomp2:i386 \
    && apt-get clean -y

RUN useradd -d /home/challenge -m -s /bin/bash challenge

WORKDIR /home/challenge

COPY writeead .
COPY flag.txt .

RUN chmod -R 755 /home/challenge
RUN chmod 444 flag.txt
RUN chmod 111 writeead

RUN chown -R root:root /home/challenge

USER challenge
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:./writeead,stderr"]
EXPOSE 9999
