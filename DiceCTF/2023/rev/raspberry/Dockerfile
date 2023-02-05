FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y \
    git python3 python3-pip graphviz

RUN python3 -m pip install graphviz antlr4-python3-runtime==4.9.1

RUN git clone https://github.com/tech-srl/RASP.git

COPY run.py ./run.py
COPY berry.rasp ./berry.rasp

ENTRYPOINT python3 run.py
