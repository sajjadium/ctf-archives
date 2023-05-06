FROM ubuntu:latest
RUN apt update && apt install -y socat && mkdir /harmony
WORKDIR /harmony
COPY run.sh ./run.sh
COPY harmony ./harmony
COPY channels ./channels
EXPOSE 5000
ENTRYPOINT ["socat", "tcp-l:5000,reuseaddr,fork", "EXEC:/harmony/run.sh,stderr"]

