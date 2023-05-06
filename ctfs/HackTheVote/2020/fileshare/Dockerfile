# NOTE: the container is provided solely for your debugging convenience should you choose to use it
# the actual challenge setup should be identical, except:
#  its a normal ubuntu 20.04 box, not a container
#  the entrypoint binary `wrapper` is executed without any arguments
#  there is a 2 minute timeout

# docker build -t fileshare .
# docker run --privileged -itd --name fileshare -p 1717:1717 -p 3434:3434 fileshare

FROM ubuntu:20.04

# just so tzdata installs without complaining
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install xinetd gdb python3 -y

COPY wrapper fileshare cleaner.py flag /
RUN mv flag flag-$(head -c 32 /dev/urandom | sha256sum | cut -d ' ' -f1)
RUN tar czhf /libs.tar.gz lib/x86_64-linux-gnu/libc.so.6 lib64/ld-linux-x86-64.so.2 lib/x86_64-linux-gnu/libpthread.so.0 lib64/ld-linux-x86-64.so.2 bin/sh

COPY xinetd.conf /etc/xinetd.d/chall
RUN echo '#!/bin/sh\nexec /wrapper -p 3434' > /chall && chmod +x /chall
RUN echo '#!/bin/sh\npython3 /cleaner.py &\nexec xinetd -dontfork' > /init && chmod +x /init

ENTRYPOINT ["/init"]
