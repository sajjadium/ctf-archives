FROM ubuntu:latest

RUN apt-get update -y \
    && apt-get install -y socat libseccomp2 \
    && apt-get clean -y

RUN useradd -d /home/challenge -m -s /bin/bash challenge

WORKDIR /home/challenge

COPY stackless .
COPY flag.txt .

RUN chmod -R 755 /home/challenge
RUN chmod 444 flag.txt
RUN chmod 111 stackless

RUN chown -R root:root /home/challenge

USER challenge
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:./stackless,stderr"]
EXPOSE 9999
