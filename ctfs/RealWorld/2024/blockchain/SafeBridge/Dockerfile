FROM ghcr.io/foundry-rs/foundry:latest AS foundry

COPY project /project

RUN apk add --no-cache nodejs npm
RUN cd /project && npm i && \
    forge build --out /artifacts/out --cache-path /artifacts/cache

FROM python:3.11.7-slim as challenge

RUN apt-get update && \
    apt-get install -y curl git socat && \
    rm -rf /var/lib/apt/lists/*

ENV FOUNDRY_DIR=/opt/foundry

ENV PATH=${FOUNDRY_DIR}/bin/:${PATH}

RUN curl -L https://foundry.paradigm.xyz | bash && \
    foundryup

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /home/ctf

COPY . challenge
COPY --from=foundry /artifacts /artifacts
COPY --from=foundry /project/node_modules challenge/project/node_modules

FROM challenge as relayer

ENTRYPOINT [ "python3", "-u", "challenge/relayer.py" ]
