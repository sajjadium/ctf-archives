FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install -y socat

RUN useradd -d /home/challenge -m -s /bin/bash challenge

WORKDIR /home/challenge

COPY flag.txt .
COPY all_patched_up .

RUN chmod -R 755 /home/challenge
RUN chmod 444 flag.txt
RUN chmod 555 all_patched_up

RUN chown -R root:root /home/challenge

USER challenge
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:./all_patched_up,stderr"]
