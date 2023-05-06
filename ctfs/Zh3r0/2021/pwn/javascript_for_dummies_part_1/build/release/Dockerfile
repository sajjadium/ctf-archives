FROM ubuntu:20.04

RUN apt-get update && apt-get install -y libreadline-dev python3 libjemalloc2

RUN useradd -d /home/challenge/ -m -p challenge -s /bin/bash challenge
RUN echo "challenge:challenge" | chpasswd

WORKDIR /home/challenge
COPY ./libjemalloc.so.2 .
COPY ./mujs .
COPY ./run.sh .
COPY ./ynetd .
COPY ./start.sh .
COPY ./connect.py .
RUN echo "zh3r0{test_flag}" > flag
RUN chown -R root:root /home/challenge

USER challenge
EXPOSE 1337
CMD ./start.sh
