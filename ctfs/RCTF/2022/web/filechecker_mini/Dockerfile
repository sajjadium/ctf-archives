FROM ubuntu:20.04

COPY ./app /app
COPY flag /flag
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update -y \
    && apt-get install python3 -y \
    && apt install pip -y \
    && pip install waitress flask -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && chmod -R 755 /app \
    && chmod 777 /app/upload

WORKDIR /app
USER nobody
CMD ["/usr/bin/python3","app.py"]