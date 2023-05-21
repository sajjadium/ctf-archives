FROM ubuntu:22.04

RUN apt update && apt install -y socat

COPY bin/server /
COPY bin/client /

COPY setup/init.sh /
COPY setup/start_client.sh /
COPY setup/start_server.sh /

EXPOSE 5000
EXPOSE 5001

CMD /init.sh
