FROM ubuntu:22.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd ssh

RUN apt-get install -y python3 python3-pip
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple flask requests[socks] termcolor

RUN useradd -m ctf
WORKDIR /home/ctf

COPY ./start.sh /start.sh
RUN chown -R root:root /start.sh
RUN chmod +x /start.sh

USER ctf

COPY ./service.py /home/ctf

CMD ["sleep", "infinity"]
# CMD ["/start.sh"]
EXPOSE 9999
