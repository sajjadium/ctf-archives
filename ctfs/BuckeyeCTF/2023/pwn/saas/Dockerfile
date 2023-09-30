FROM ubuntu:22.04@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054 as build

RUN apt update && apt upgrade -y
RUN apt install git gcc-arm-linux-gnueabi qemu-user gdb-multiarch make wget -y

WORKDIR /build
COPY make-capstone.sh /build
RUN wget --no-verbose -O "capstone-5.0.tar.gz" "https://github.com/capstone-engine/capstone/archive/refs/tags/5.0.tar.gz"

RUN ./make-capstone.sh
COPY chal.c build.sh /build/
RUN ./build.sh


FROM ubuntu:22.04@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054 as prod_build

RUN apt update && apt upgrade -y
RUN apt install qemu-user -y

WORKDIR /app
COPY --from=build /build/chal .
COPY flag.txt ./
# Jail entrypoint
COPY run.sh run


FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c as prod

COPY --from=prod_build / /srv
