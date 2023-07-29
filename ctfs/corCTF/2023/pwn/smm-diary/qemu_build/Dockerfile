from ubuntu:20.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build git libslirp-dev

RUN echo "#!/bin/bash\ncd /qemu && \
    bash -c './configure --target-list=x86_64-softmmu && \
        make -j$(nproc)'" > build.sh

RUN chmod +x /build.sh


CMD ["/build.sh"]
