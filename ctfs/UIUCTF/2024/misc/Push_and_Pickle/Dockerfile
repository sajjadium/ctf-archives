FROM python:3.9.6

RUN apt-get update && apt-get install -y socat

WORKDIR /home/user
COPY chal.py .

CMD socat -T60 TCP-LISTEN:1337,fork,reuseaddr EXEC:"python3 -u chal.py"
