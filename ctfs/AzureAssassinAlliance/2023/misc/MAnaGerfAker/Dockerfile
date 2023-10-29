# docker build -t managerfaker:latest .
# docker run -idt -p 32107:22222 managerfaker:latest
FROM ubuntu:22.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install socat python3 python3-pip default-jre -y

WORKDIR /app
COPY ./verifier.py ./secret.py ./apksigner.jar /app
RUN chmod -R 777 /app

EXPOSE 22222

CMD ["socat", "TCP-LISTEN:22222,reuseaddr,fork", "EXEC:python3 verifier.py,nofork,stderr"]