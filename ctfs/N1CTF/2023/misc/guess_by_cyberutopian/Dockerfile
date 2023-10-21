FROM ubuntu:23.04
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && apt-get update && apt-get install -y python3 xinetd
COPY files /files
RUN chmod a+x /files/setup.sh && sh /files/setup.sh
EXPOSE 9999
CMD [ "/start.sh" ]