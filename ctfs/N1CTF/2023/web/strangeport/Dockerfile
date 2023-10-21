FROM apache/activemq-classic:5.17.5
RUN apt-get update
RUN apt-get install wget curl -y
COPY ./files/SimpleAPI-1.0-SNAPSHOT.jar /root/SimpleAPI-1.0-SNAPSHOT.jar
COPY ./files/start.sh /root/start.sh
COPY ./files/flag /flag
ENTRYPOINT ["/bin/bash", "/root/start.sh"]
