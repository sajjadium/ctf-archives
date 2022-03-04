FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get -y update && \
    apt-get install -y libfuse3-3 fuse3 lib32z1 xinetd apt-transport-https python3

RUN useradd -m ctf &&  \
    echo "service ctf\n{\n    disable = no\n    socket_type = stream\n    protocol    = tcp\n    wait        = no\n    user        = root\n    type        = UNLISTED\n    port        = 9999\n    bind        = 0.0.0.0\n    server      = /start.sh\n    banner_fail = /etc/banner_fail\n    # safety options\n    per_source    = 10 # the maximum instances of this service per source IP address\n    #rlimit_cpu    = 1 # the maximum number of CPU seconds that the service may use\n    #rlimit_as  = 1024M # the Address Space resource limit for the service\n    #access_times = 2:00-9:00 12:00-24:00\n}" > /etc/xinetd.d/ctf && \
    echo "#!/bin/bash\n/etc/init.d/xinetd start\nsleep infinity" > /root/start.sh && \
    chmod +x /root/start.sh

RUN mkdir /chroot && \
	chown root:ctf /chroot && \
	chmod 755 /chroot && \
	cp -R /lib* /chroot && \
	mkdir /chroot/usr && \
	cp -R /usr/lib* /chroot/usr && \
	mkdir /chroot/bin && \
	cp /bin/timeout /bin/base64 /bin/echo /bin/chmod /bin/mv /bin/ls /bin/rm /bin/touch /bin/sh /bin/mkdir /bin/rmdir /bin/cat /chroot/bin && \
	mkdir /chroot/mnt /chroot/rwdir && \
	chown ctf:ctf /chroot/mnt /chroot/rwdir

COPY ./start.sh ./d3fuse /

RUN echo flag{fake_flag} > /flag && \
    chmod +x /start.sh /d3fuse

CMD "/root/start.sh"
