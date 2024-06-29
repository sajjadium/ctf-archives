# Use an Ubuntu base image
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
# Install QEMU and MIPS cross-compiler
RUN apt-get update && apt-get install -y \
    qemu-user \
    qemu-user-static \
    build-essential \
    socat \
    gcc-mips-linux-gnu

# Set the working directory
WORKDIR /usr/src/app
# gcc-mips-linux-gnu
# Copy your MIPS executable into the container
COPY Makefile .
COPY backup-power.c .
COPY flag.txt .

# RUN make
COPY backup-power .
# Default command to run when the container starts
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"qemu-mips ./backup-power"
