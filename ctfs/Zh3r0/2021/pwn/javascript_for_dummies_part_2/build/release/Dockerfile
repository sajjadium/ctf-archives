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
COPY ./flag ./

RUN chmod +x ./start.sh
RUN chmod +x ./ynetd
RUN chmod +x ./connect.py
RUN chmod +x ./run.sh
RUN chmod +x ./mujs



RUN chown -R root:root /home/challenge

EXPOSE 1337
USER challenge
CMD ./start.sh
