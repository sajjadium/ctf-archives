# yoinked from https://github.com/google/google-ctf/blob/master/2022/quals/pwn-d8/

FROM ubuntu:22.04 as build

# install required deps
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -yq --no-install-recommends build-essential git ca-certificates python3-pkgconfig curl python3

# install depot_tools
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git /opt/depot_tools
ENV PATH="/opt/depot_tools:${PATH}"

RUN mkdir /build
COPY remove_globals.patch /build/remove_globals.patch

RUN cd /build && fetch v8 && cd v8 && git checkout 29131d5e3ea9cbfeae3e6dc3fd6c4439f0ac4bde && git apply ../remove_globals.patch && gclient sync

# build with enabled memory_corruption_api
RUN cd /build/v8 && gn gen out/release --args='is_debug=false target_cpu="x64" v8_enable_sandbox=true v8_expose_memory_corruption_api=true' && \
    autoninja -C out/release d8