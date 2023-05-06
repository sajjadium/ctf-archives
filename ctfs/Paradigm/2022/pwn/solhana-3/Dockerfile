FROM rust:1.60
EXPOSE 3000

# update our shit
RUN apt update && apt upgrade -y
RUN apt install sqlite3 daemonize

RUN mkdir /ctf
WORKDIR /ctf

# install dependencies for the project so they can be cached
RUN cargo new --bin server
WORKDIR ./server
COPY ./server/Cargo.lock ./Cargo.lock
COPY ./server/Cargo.toml ./Cargo.toml
run cargo build --release
RUN rm -r src/

# copy over the project and build it properly
COPY ./keys /ctf/keys
COPY ./server/src ./src
RUN rm ./target/release/deps/server*
RUN cargo build --release

# copy over rest of the shit
COPY ./docker /ctf/docker
COPY ./elf /ctf/elf

# init the player database
RUN /ctf/docker/init_db.sh

CMD ["/ctf/docker/start_server.sh"]
