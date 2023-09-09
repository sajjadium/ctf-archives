FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY run.sh server.py .

ENTRYPOINT ["socat", "TCP-LISTEN:5000,fork,reuseaddr", "EXEC:'timeout 240 ./run.sh',stderr"]
