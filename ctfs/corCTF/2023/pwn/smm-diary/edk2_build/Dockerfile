FROM ubuntu:20.04 as ubuntu-build

RUN apt -y update
RUN apt -y install build-essential uuid-dev iasl git python-is-python3 wget

RUN wget http://www.nasm.us/pub/nasm/releasebuilds/2.15.05/nasm-2.15.05.tar.bz2 && \
    tar xfj nasm-2.15.05.tar.bz2 && \
    cd nasm-2.15.05/ && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local/ && \
    make -j$(nproc) && make install

RUN echo "#!/bin/bash\ncd /build && \
    bash -c 'source edksetup.sh && \
        make -C BaseTools/Source/C -j $(nproc) && \
        build -p OvmfPkg/OvmfPkgX64.dsc -a X64 -t GCC5 -D SMM_REQUIRE=TRUE'" > build.sh

RUN chmod +x /build.sh

CMD ["/build.sh"]