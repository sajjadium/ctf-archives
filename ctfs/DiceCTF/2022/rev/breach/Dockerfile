FROM ubuntu:20.04

COPY breach /app/breach
COPY breach.bin /app/breach.bin

RUN echo "PWN_FLAG" > /app/flag.txt

CMD /app/breach /app/breach.bin
