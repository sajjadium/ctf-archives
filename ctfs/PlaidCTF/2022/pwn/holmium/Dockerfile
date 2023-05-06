FROM ubuntu:focal-20220316

WORKDIR /pwn
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY [ "holmium", "flag.txt", "docker-main", "./" ]

CMD [ "./docker-main" ]
