FROM ubuntu:22.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list && \
    sed -i "s/http:\/\/security.ubuntu.com/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list

RUN apt-get -y update && \
    apt-get -y dist-upgrade && \
    apt-get -y install xinetd python3 lib32z1 netcat libfuse3-dev g++ gcc cmake pkg-config fuse3

COPY ./src /root/src

RUN cd /root/src && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make myfuse &&\
    make mkfs.myfuse &&\
    cp mkfs/mkfs.myfuse /usr/bin &&\
    cp myfuse /usr/bin &&\
    echo "user_allow_other" >> /etc/fuse.conf &&\
    dd if=/dev/zero of=/cfs.disk bs=512 count=40000 &&\
    yes "yes" | mkfs.myfuse /cfs.disk

RUN groupadd -g 1000 ctf && \
    useradd -g ctf -u 1000 ctf -s /bin/bash && \
    groupadd -g 1001 fuse && \
    useradd -g fuse -u 1001 fuse -s /bin/bash

COPY ./start.sh /start.sh
COPY ./flag /flag
COPY ./fuse_server.sh /usr/bin/fuse_server
COPY ./spawner /spawner
COPY ./userinit.sh /userinit.sh

RUN chmod 550 /spawner &&\
    chmod 555 /usr/bin/fuse_server &&\
    chmod 711 /usr/bin/myfuse &&\
    chmod 711 /usr/bin/mkfs.myfuse &&\
    chmod 444 /flag &&\
    chmod 711 /start.sh &&\
    echo "service ctf\n{\n    disable = no\n    socket_type = stream\n    protocol    = tcp\n    wait        = no\n    user        = root\n    type        = UNLISTED\n    port        = 9999\n    bind        = 0.0.0.0\n    server      = /start.sh\n    banner_fail = /etc/banner_fail\n    # safety options\n    per_source    = 10 # the maximum instances of this service per source IP address\n    #rlimit_cpu    = 1 # the maximum number of CPU seconds that the service may use\n    #rlimit_as  = 1024M # the Address Space resource limit for the service\n    #access_times = 2:00-9:00 12:00-24:00\n}" > /etc/xinetd.d/ctf 
#    echo "#!/bin/sh\n/usr/sbin/xinetd -dontfork" > /root/start.sh &&\
#    chmod +x /root/start.sh


EXPOSE 9999
# CMD /root/start.sh
CMD ["/usr/sbin/xinetd","-dontfork"]
