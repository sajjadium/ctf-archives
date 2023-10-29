FROM ubuntu:22.04

RUN apt update -y
RUN apt install -y wget openjdk-19-jdk unzip socat

USER nobody

WORKDIR /tmp
RUN wget http://archive.apache.org/dist/logging/log4j/2.14.1/apache-log4j-2.14.1-bin.zip
RUN unzip apache-log4j-2.14.1-bin.zip

COPY Main.java .
RUN javac -cp '/tmp/apache-log4j-2.14.1-bin/log4j-api-2.14.1.jar:/tmp/apache-log4j-2.14.1-bin/log4j-core-2.14.1.jar' Main.java
CMD socat -v tcp-listen:1337,fork,reuseaddr system:"java -cp '.:/tmp/apache-log4j-2.14.1-bin/log4j-api-2.14.1.jar:/tmp/apache-log4j-2.14.1-bin/log4j-core-2.14.1.jar' Main",stderr
