FROM rust@sha256:0372c87d4372dc1ae23caaf287f643f7c5ca799b40405efbb1bdf67588cc2629

RUN apt-get update && apt-get install -qy libudev-dev

WORKDIR /app
COPY server ./server
COPY program ./program

RUN sh -c "$(curl -sSfL https://release.solana.com/v1.10.32/install)"
ENV PATH="/root/.local/share/solana/install/active_release/bin:${PATH}"

RUN mkdir -p /app/challenge

COPY flag.txt /app/challenge/flag.txt

RUN cd server && make
RUN cd program && make

WORKDIR /app/challenge

CMD [ "./utility-payment-server" ]
