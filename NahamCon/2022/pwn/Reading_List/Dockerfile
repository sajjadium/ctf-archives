FROM docker.io/ubuntu:20.04

RUN apt-get update -y \
    && apt-get install -y socat \
    && apt-get clean -y

RUN useradd -d /home/challenge -m -s /bin/bash challenge

WORKDIR /home/challenge

COPY reading_list .
COPY flag.txt .

RUN chmod -R 755 /home/challenge
RUN chmod 444 flag.txt
RUN chmod 111 reading_list

RUN chown -R root:root /home/challenge

USER challenge
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:./reading_list,stderr"]
EXPOSE 9999
