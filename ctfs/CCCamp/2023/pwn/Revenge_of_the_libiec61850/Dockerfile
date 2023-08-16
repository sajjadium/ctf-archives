# docker build -t honk-honk . && docker run --rm -it -p1024:1024 honk-honk
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ctf@127.0.0.1 -p 1024
FROM ubuntu:22.04

RUN set -x && \
    apt-get update && \
    apt-get install -y xinetd cmake build-essential unzip git dropbear rsync openssh-client libcap2-bin python3 python3-pip && apt-get clean

RUN useradd -d /home/ctf/ -m -s /bin/bash ctf && passwd -d ctf

WORKDIR /home/ctf

# Starts dropbear SSH and GOOSE subscriber
COPY run.sh .

# Clone libiec61850 and compile it
RUN git clone https://github.com/mz-automation/libiec61850.git && cd libiec61850 && git checkout f41667367a0c9841400bd3e50415db8a5301b7ad
WORKDIR /home/ctf/libiec61850/
RUN mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release  -DBUILD_EXAMPLES=ON -DCMAKE_EXE_LINKER_FLAGS="-no-pie" -DCMAKE_C_FLAGS="-fno-stack-protector" ..
WORKDIR /home/ctf/libiec61850/build/
RUN make -j4

# Install pwntools
RUN python3 -m pip install pwntools

# Copy flag and chmod it
COPY flag /
RUN chmod 600 /flag

EXPOSE 1024

# Go! :)
CMD ["/bin/sh","/home/ctf/run.sh"]
