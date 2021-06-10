FROM ubuntu:16.04

## 更改源及安装必要的软件
#RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/cn.archive.ubuntu.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y libpcre3 libpcre3-dev
#RUN apt-get install -y lib32z1 build-essential
RUN apt-get install -y python python-pip python-dev
RUN apt-get install -y unzip

## 添加用户
RUN useradd -m ctf

## 初始化环境
WORKDIR /home/ctf

## 复制源文件，编译
COPY ./bin/ /home/ctf/
RUN unzip /home/ctf/Lo-runner-master.zip
RUN cd /home/ctf/Lo-runner-master/ && python setup.py install
RUN rm -rf /home/ctf/Lo-runner-master*
RUN pip install flask uwsgi supervisor
RUN chown -R root:ctf /home/ctf
RUN chown ctf:ctf /home/ctf
RUN chmod -R 750 /home/ctf
RUN chmod 740 /home/ctf/flag
RUN chmod +x /home/ctf/server.py


COPY ./supervisord.conf /etc/supervisord.conf


CMD exec /bin/bash -c "supervisord -c /etc/supervisord.conf; trap : TERM INT; sleep infinity & wait"

EXPOSE 11111
