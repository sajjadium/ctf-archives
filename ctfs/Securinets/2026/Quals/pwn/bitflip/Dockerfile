FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN useradd -m ctf
COPY main libc.so.6 ld-linux-x86-64.so.2 flag.txt ./
RUN chmod 0555 main ld-linux-x86-64.so.2 && chmod 0444 libc.so.6 flag.txt
USER ctf
EXPOSE 10001
CMD ["socat", "TCP-LISTEN:10001,reuseaddr,fork", "EXEC:timeout 15 ./main"]
