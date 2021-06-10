# docker build -t candles2 .
# docker run -p 3451:3451 -d --name candles2 candles2

FROM ubuntu:20.04

# just so tzdata installs without complaining
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install xinetd gdb -y

RUN useradd -m candles
COPY candles leakguard.so run.sh flag /home/candles/
COPY xinetd.conf /etc/xinetd.d/candles

RUN chown -R root:candles /home/candles
RUN chmod -R 750 /home/candles
ENTRYPOINT ["xinetd", "-dontfork"]
