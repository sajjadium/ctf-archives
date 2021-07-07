From openjdk:8u232-slim

RUN sed -i 's/deb.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list \
    && apt-get update -y \
    && apt-get install curl -y \
    && useradd ctf \
    && mkdir /opt/app

COPY rmiclient.jar /opt/app
COPY flag /flag

WORKDIR /opt/app

USER ctf
CMD ["java", "-jar", "/opt/app/rmiclient.jar"]