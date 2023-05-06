FROM openjdk:11-slim-buster

ARG name
ARG port

RUN apt-get update -y; apt-get install socat -y
COPY flag.txt /pwn/flag.txt
COPY src /pwn
WORKDIR /pwn
RUN javac *.java
ENV JDK_JAVA_OPTIONS="-Xmx64M"

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'java Challenge',stderr" > /pwn/docker_entrypoint.sh

ENTRYPOINT ["sh", "/pwn/docker_entrypoint.sh"]
