FROM debian:unstable-20211220-slim AS build

RUN echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20220112T093851Z unstable main" > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y cmake g++ zlib1g-dev libfreetype-dev libfontconfig-dev libpng-dev
ADD xpdf-4.03.tar.gz /tmp/
RUN cd /tmp/xpdf-4.03 && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro" .. && \
    make -j$(nproc)

FROM debian:unstable-20211220-slim
RUN echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20220112T093851Z unstable main" > /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y zlib1g libfreetype6 libfontconfig1 libpng16-16 && \
    # Who don't like some free fonts?
    apt-get install -y fonts-arkpandora fonts-noto fonts-dejavu fonts-font-awesome fonts-lato fonts-powerline gsfonts && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY --from=build /tmp/xpdf-4.03/build/xpdf/pdftohtml /usr/local/bin/
RUN mkdir -p /run/secrets && echo 'rwctf{flag placeholder}' > /run/secrets/flag

ENTRYPOINT [ "/bin/sh", "-c", "/usr/local/bin/pdftohtml \"$@\"", "--" ]
