FROM debian:bookworm-20231218
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install openssl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ./heater/heater . 
COPY ./heater/run.sh . 
COPY flag2 flag
COPY wait_for_can.sh .
COPY pubkey .

CMD ./run.sh
