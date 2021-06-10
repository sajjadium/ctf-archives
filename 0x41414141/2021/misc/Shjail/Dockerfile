FROM ubuntu:latest

RUN apt-get update -y \
    && apt-get install -y socat python3.8 \
    && apt-get clean -y

RUN useradd -d /home/challenge -m -s /bin/bash challenge

COPY deps/limits.conf /etc/security/limits.d/90-challenge.conf

WORKDIR /home/challenge

COPY src/shjail.sh .
COPY src/flag.txt .

RUN chmod -R 755 /home/challenge
RUN chmod 444 flag.txt
RUN chmod 555 shjail.sh

RUN chown -R root:root /home/challenge

USER challenge
CMD ["socat", "TCP-LISTEN:9998,reuseaddr,fork", "EXEC:./shjail.sh,stderr"]
EXPOSE 9998
EXPOSE 4545
