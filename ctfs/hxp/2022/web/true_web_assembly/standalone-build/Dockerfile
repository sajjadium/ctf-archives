# docker build -t asmbb-build .

# This would produce an archive in /asmbb-challenge.tar.gz which would contain a built website.

FROM ubuntu:20.04

# Get necessary dependencies to build
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y wget make gcc cmake git g++ sqlite3

# Get flat assembler
RUN wget https://flatassembler.net/fasm-1.73.30.tgz -O fasm.tgz && \
	/bin/bash -c "echo '75195051a5881dbbbe0f0401161e937f8a36bb42d3470fc4869da14fd2c2f101 fasm.tgz' | sha256sum --check" && \
	tar -xf fasm.tgz

# Get source files for asmbb
RUN wget https://asm32.info/fossil/asmbb/tarball/4c91cddaec/asmbb-4c91cddaec.tar.gz -O asmbb.tar.gz && \
	/bin/bash -c "echo 'b1e621d1ae988b35e836ec9142ccc6ce6cf7c24a090c4d973894770a62fa4ddc asmbb.tar.gz' | sha256sum --check" && \
	tar -xf asmbb.tar.gz || true && \
	mv asmbb-* asmbb

# Get source files for freshlib
# AsmBB uses functions from freshlib
RUN wget https://fresh.flatassembler.net/fossil/repo/fresh/tarball/6636a57441/Fresh+IDE-6636a57441.tar.gz -O fresh.tar.gz && \
	/bin/bash -c "echo '5ba395b0e957536bd66abc572414085aab5f2a527d28214881bbba72ec53e00d fresh.tar.gz' | sha256sum --check" && \
	tar -xf fresh.tar.gz && \
	mv Fresh* Fresh

# Build the asmbb engine
RUN lib=/Fresh/freshlib TargetOS=Linux /fasm/fasm -m 200000 /asmbb/source/engine.asm /engine

# Build sqlite table
RUN sqlite3 /asmbb/board.sqlite < /asmbb/source/create.sql

# Get glessc. This is only necessary for building the asmbb templates.
RUN git clone https://github.com/BramvdKroef/clessc.git && cd clessc && mkdir build && cd build && cmake .. && make -j4
RUN cd /asmbb/www/templates && PATH="$PATH:/clessc/build" ./build_styles.sh

# Package everything
# NOTE: we don't build ld-musl-i386.so and libsqlite3.so to avoid even more clutter.
RUN mkdir /asmbb-challenge && cd /asmbb-challenge && cp /engine . && cp -r /asmbb/www/* .
COPY libsqlite3.so /asmbb-challenge/.
COPY ld-musl-i386.so /asmbb-challenge/.
RUN cp /asmbb/board.sqlite /asmbb-challenge/.
RUN tar -czvf /asmbb-challenge.tar.gz /asmbb-challenge

CMD sh

