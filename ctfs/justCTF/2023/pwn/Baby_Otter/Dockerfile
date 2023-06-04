FROM rust:latest

RUN apt-get update && apt-get install -qy clang libudev-dev nodejs npm tmux vim neovim git netcat zsh nano wget cmake gcc libssl-dev libclang-dev curl libpq-dev screen
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

RUN rustup component add rustfmt
RUN rustup update stable

WORKDIR /home

RUN rustup update stable
RUN wget https://github.com/MystenLabs/sui/releases/download/devnet-v1.2.0/sui
RUN chmod +x sui 
RUN mv sui /bin
RUN git clone https://github.com/MystenLabs/sui.git
RUN git clone https://github.com/otter-sec/sui-ctf-framework.git

WORKDIR /work/framework
ADD ./framework/Cargo.toml .

ARG FLAG
ENV FLAG=$FLAG

RUN mkdir src
RUN echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

ADD ./framework /work/framework

WORKDIR /work/framework/chall
RUN sui move build

WORKDIR /work/framework

# refresh from dummy
RUN touch src/main.rs
RUN cargo build --locked --release

CMD cargo r --release
