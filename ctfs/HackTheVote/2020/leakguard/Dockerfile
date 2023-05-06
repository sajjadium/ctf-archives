# docker build -t candles .
# docker run -p 1734:1734 -d --name candles candles

FROM ubuntu:18.04

RUN apt-get update -y && apt-get install xinetd -y

RUN useradd -m candles
COPY candles leakguard.so run.sh flag /home/candles/
COPY xinetd.conf /etc/xinetd.d/candles

RUN chown -R root:candles /home/candles
RUN chmod -R 750 /home/candles
ENTRYPOINT ["xinetd", "-dontfork"]
