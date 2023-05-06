FROM ubuntu:20.04

WORKDIR /app
COPY ./corchat_server .
COPY ./flag.txt .

RUN useradd -m ctf
USER ctf

EXPOSE 5000
CMD ["./corchat_server", "5000"]
