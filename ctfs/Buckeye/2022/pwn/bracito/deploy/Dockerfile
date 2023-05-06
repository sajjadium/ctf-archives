
# Install nsjail from source
FROM ubuntu:22.04 as nsjail-builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y \
autoconf \
bison \
flex \
gcc \
g++ \
git \
libprotobuf-dev \
libnl-route-3-dev \
libtool \
make \
pkg-config \
protobuf-compiler \
uidmap

RUN git clone https://github.com/google/nsjail && \
cd nsjail && \
make -j8 && \
mv nsjail /bin && \
cd / && \
rm -rf nsjail

# Build the challenge
FROM ubuntu:22.04 as builder
RUN apt-get -y update && apt-get install -y gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu binutils-aarch64-linux-gnu-dbg build-essential curl && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN rustup target add aarch64-unknown-linux-gnu

COPY ./app/ /code/
WORKDIR /code/

COPY cargo-config /root/.cargo/config
RUN cargo build --target  aarch64-unknown-linux-gnu --release


FROM ubuntu:22.04@sha256:dda6886d8d153a2d86f046c9335123c6151d83fd63e446b752ed8d9da261205d
RUN apt-get update && apt-get install -y qemu-user qemu-user-static gcc-aarch64-linux-gnu libprotobuf23 libnl-route-3-200 && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf && \
mkdir /chroot/ && \
chown root:ctf /chroot && \
chown root:ctf /home/ctf && \
chmod 770 /chroot

WORKDIR /home/ctf/app
COPY --from=nsjail-builder /usr/bin/nsjail /usr/bin/
COPY --from=builder /code/target/aarch64-unknown-linux-gnu/release/arm-vm /home/ctf/app/chall

COPY flag.txt ./
COPY jail.cfg run.sh /

RUN chown -R root:ctf . && \
chmod 440 flag.txt

CMD /run.sh
