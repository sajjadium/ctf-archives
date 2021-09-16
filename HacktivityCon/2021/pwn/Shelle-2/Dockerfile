FROM ubuntu:latest

RUN apt-get update -y \
    && apt-get install -y socat \
    && apt-get clean -y

RUN useradd -d /home/challenge -m -s /bin/bash challenge

WORKDIR /home/challenge

COPY shelle-2 .
COPY flag.txt .

RUN chmod -R 755 /home/challenge
RUN chmod 444 flag.txt
RUN chmod 111 shelle-2

RUN chown -R root:root /home/challenge

USER challenge
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:./shelle-2,stderr"]
EXPOSE 9999
