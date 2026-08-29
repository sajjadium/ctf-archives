FROM ubuntu@sha256:678c6550cc43645e08669028bc177f50be4e7c5b8cca677067b1914d4afc7a03

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash ctf

COPY redis-cli run.sh /home/ctf/
COPY entrypoint.sh /usr/local/bin/redis-cli-entrypoint

WORKDIR /home/ctf

RUN chmod 0555 redis-cli run.sh /usr/local/bin/redis-cli-entrypoint \
    && chown root:root /home/ctf /home/ctf/redis-cli /home/ctf/run.sh \
        /usr/local/bin/redis-cli-entrypoint \
    && chmod 0555 /home/ctf

EXPOSE 1337

ENTRYPOINT ["redis-cli-entrypoint"]
