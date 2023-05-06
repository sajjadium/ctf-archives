FROM ubuntu:18.04

RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc -y
RUN apt-get install socat -y

COPY ./files/* /opt/
WORKDIR /opt/

RUN gcc gamblingProblem.c -o gamblingProblem -fstack-protector-all -Wl,-z,now,-z,relro
RUN chmod 555 gamblingProblem
RUN chmod 444 flag.txt

CMD socat TCP-LISTEN:9124,reuseaddr,fork EXEC:"./gamblingProblem",su=nobody && fg
