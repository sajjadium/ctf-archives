FROM python:slim@sha256:f41a75c9cee9391c09e0139f7b49d4b1fbb119944ec740ecce4040626dc07bed

RUN apt update && apt install socat -y && pip install pycryptodome

COPY server.py /

CMD socat TCP-LISTEN:1338,fork EXEC:/server.py
