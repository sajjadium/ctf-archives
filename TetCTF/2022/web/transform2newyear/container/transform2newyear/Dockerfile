FROM ubuntu:latest
MAINTAINER peterjson

RUN apt-get update -y && apt-get upgrade -y && apt-get install supervisor openjdk-8-jre-headless -y

RUN useradd service && mkdir /home/service

# secret place to store flag :)
RUN export RAN_DIR=/`tr -dc T-Zt-z0-9 </dev/urandom | head -c 10 ; echo ''`/ && mkdir -p $RAN_DIR && cd $RAN_DIR && echo "TetCTF{<?TetCTF ?> sample flag, :) }" > flag_`tr -dc T-Zt-z0-9 </dev/urandom | head -c 5 ; echo ''`.txt

RUN chown -R service:root /home/service/ && chmod 770 -R /home/service/

COPY ./container/transform2newyear/supervisor.conf /etc/supervisor.conf

COPY ./container/transform2newyear/transformer-0.0.1-SNAPSHOT.jar /home/service/transformer-0.0.1-SNAPSHOT.jar

EXPOSE 8080

CMD ["supervisord", "-c", "/etc/supervisor.conf"]
