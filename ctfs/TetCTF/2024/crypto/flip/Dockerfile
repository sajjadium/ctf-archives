FROM python:3.10-bookworm

RUN apt update && apt install -y socat

RUN useradd -m -U flip
USER flip:flip
WORKDIR /home/flip

COPY . .

CMD socat -T 30 TCP-LISTEN:31339,reuseaddr,fork EXEC:"python -u main.py"