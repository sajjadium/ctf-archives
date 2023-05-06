FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 socat

COPY proxy.py .
COPY flag .
COPY CoroutineCTFChal .

EXPOSE 12345
CMD socat TCP-LISTEN:12345,reuseaddr,fork EXEC:"python3 proxy.py"