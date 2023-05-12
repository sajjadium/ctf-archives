FROM ubuntu:22.04

RUN apt update && apt upgrade -y

RUN apt-get install -y socat
RUN apt-get install -y libssl-dev
RUN apt install openjdk-19-jdk -y

COPY SmallStringStorage.jar /SmallStringStorage.jar

CMD ["socat", "-T120", "TCP-LISTEN:1234,reuseaddr,fork", "EXEC:java -jar SmallStringStorage.jar,pty,raw,stderr,echo=0"]