FROM rust
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install socat -y
WORKDIR /app
COPY . .
ENV FLAG="0xL4ugh{fake_flag}"
RUN cargo build --release
RUN chmod +x ./start.sh

ENTRYPOINT  ["./start.sh"]
