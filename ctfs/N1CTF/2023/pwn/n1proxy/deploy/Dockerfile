FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade &&\
    apt-get install -y lib32z1 xinetd build-essential

RUN useradd -m ctf

WORKDIR /home/ctf

COPY ./target/release/n1proxy_server /home/ctf/n1proxy_server

RUN chown -R root:ctf /home/ctf && chmod -R 750 /home/ctf && \
    echo "flag{test}" > /home/ctf/flag && \
    chmod 740 /home/ctf/flag && chmod o+r /home/ctf/flag && chmod a+x /home/ctf/n1proxy_server

CMD exec /bin/bash -c "rm -rf /tmp/n1proxy; cd /home/ctf/ ; su ctf -c \"/usr/bin/timeout -s SIGKILL 1800 ./n1proxy_server 23333\""

EXPOSE 23333
