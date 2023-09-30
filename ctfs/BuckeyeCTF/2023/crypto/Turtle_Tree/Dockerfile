FROM python:3-slim

RUN apt-get update && \
apt-get install -y socat && \
pip3 install --no-cache-dir cryptography

WORKDIR /opt/app
COPY main.py merkle_tree.py proof.py util.py flag.py ./
CMD socat -d -d -s TCP-LISTEN:1024,reuseaddr,fork EXEC:'timeout 30 python -u /opt/app/main.py',stderr
