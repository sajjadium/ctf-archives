FROM ubuntu:22.04

WORKDIR /app
COPY ./server.bin .
COPY ./flag.txt .

RUN useradd -m ctf
USER ctf

EXPOSE 5000
CMD ["./server.bin", "5000"]
