From openjdk:8u265-slim

RUN sed -i 's/deb.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list \
    && apt-get update -y \
    && apt-get install curl -y \
    && useradd ctf \
    && mkdir /opt/app

COPY spider.jar /opt/app

WORKDIR /opt/app

EXPOSE 8080

USER ctf
CMD ["java", "-jar", "/opt/app/spider.jar"]