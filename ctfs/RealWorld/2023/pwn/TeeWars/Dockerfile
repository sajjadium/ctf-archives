FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y rsync xorg wget unzip && \
    apt-get install -y lib32z1 xinetd iputils-ping build-essential cmake git libfreetype6-dev libsdl2-dev libpnglite-dev libwavpack-dev python3 curl xvfb rustc


RUN curl -s https://www.libsdl.org/release/SDL2-2.0.10.tar.gz -o SDL2-2.0.10.tar.gz && \
    tar xf SDL2-2.0.10.tar.gz && \
    cd /SDL2-2.0.10 && ./configure && make -j && make install && \
    cd / && rm -rf /SDL2-2.0.10 SDL2-2.0.10.tar.gz

RUN useradd -m rwctf

WORKDIR /home/rwctf

RUN cd /home/rwctf && \
    wget  https://github.com/teeworlds/teeworlds/releases/download/0.7.5/teeworlds-0.7.5-src.zip && \
    unzip ./teeworlds-0.7.5-src.zip -d  /home/rwctf/ && \
    sed -i '155s/.*/  #add_c_compiler_flag_if_supported(OUR_FLAGS -fstack-protector-strong)/' /home/rwctf/teeworlds-0.7.5-src/CMakeLists.txt && \
    sed -i '158s/.*/  #add_c_compiler_flag_if_supported(OUR_FLAGS -fstack-clash-protection)/' /home/rwctf/teeworlds-0.7.5-src/CMakeLists.txt && \
    sed -i '161s/.*/  #add_c_compiler_flag_if_supported(OUR_FLAGS -fcf-protection)/' /home/rwctf/teeworlds-0.7.5-src/CMakeLists.txt && \
    mkdir -p /home/rwctf/teeworlds-0.7.5-src/build

RUN cd /home/rwctf/teeworlds-0.7.5-src/build && \
    cmake .. -DCMAKE_BUILD_TYPE=DEBUG -DCMAKE_CXX_FLAGS_DEBUG="-g -O2 -fno-stack-protector -no-pie -z lazy" && \
    make -j `nproc` && \
    chmod +x /home/rwctf/teeworlds-0.7.5-src/build/teeworlds && \
    cp /home/rwctf/teeworlds-0.7.5-src/build/teeworlds /home/rwctf/ && \
    echo "rwctf{this_is_a_sample_flag}" > /home/rwctf/flag

COPY ./rwctf.rs /home/rwctf/

RUN cd /home/rwctf && \
    rustc ./rwctf.rs -o rwctf

CMD ["/home/rwctf/rwctf"]

