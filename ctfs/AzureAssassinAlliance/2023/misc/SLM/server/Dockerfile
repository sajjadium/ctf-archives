FROM ubuntu:22.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd ncat

RUN apt-get install -y python3 python3-pip

RUN useradd -m ctf
WORKDIR /home/ctf

COPY requirements.txt /home/ctf/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /home/ctf/requirements.txt

COPY flag /flag
COPY server.py /home/ctf/server.py
COPY start.sh /start.sh

RUN chown -R root:root /flag /tmp /start.sh /home/ctf/server.py
RUN rm /home/ctf/.profile /home/ctf/.bashrc /home/ctf/.bash_logout
RUN chmod +x /start.sh
RUN chmod a-w /home/ctf /tmp

USER ctf
CMD ["/start.sh"]
EXPOSE 9999