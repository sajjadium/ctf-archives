FROM buildpack-deps@sha256:060c71d6a2053b21c4c5e8cd20ccd50f587f3dea37321b1af7f050c80e0ac040

WORKDIR /deps

RUN wget https://ziglang.org/builds/zig-linux-x86_64-0.11.0-dev.2477+2ee328995.tar.xz \
    && wget http://ftp.gnu.org/gnu/mtools/mtools-4.0.43.tar.gz \
    && tar -xvf zig-linux-x86_64-0.11.0-dev.2477+2ee328995.tar.xz \
    && tar -xvf mtools-4.0.43.tar.gz \
    && mv zig-linux-x86_64-0.11.0-dev.2477+2ee328995 zig \
    && mv mtools-4.0.43 mtools
RUN cd mtools && ./configure && make
ENV PATH="/deps/mtools:/deps/zig:${PATH}"

COPY mtools.conf /etc/mtools.conf