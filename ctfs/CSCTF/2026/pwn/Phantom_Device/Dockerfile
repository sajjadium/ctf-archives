FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    libimobiledevice-1.0-6 \
    libplist-2.0-4 \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --system --create-home --shell /usr/sbin/nologin ctf

WORKDIR /challenge
COPY client /challenge/client
RUN chmod +x /challenge/client

COPY flag.txt /flag.txt
RUN chown ctf:ctf /flag.txt && chmod 0600 /flag.txt

COPY entrypoint.sh /challenge/entrypoint.sh
COPY handler.sh /challenge/handler.sh
RUN sed -i 's/\r$//' /challenge/entrypoint.sh /challenge/handler.sh \
    && chmod +x /challenge/entrypoint.sh /challenge/handler.sh

USER ctf
EXPOSE 1337
CMD ["/challenge/entrypoint.sh"]
