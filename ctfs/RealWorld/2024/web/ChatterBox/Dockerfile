# 使用带有 Java 17 的基础镜像
FROM openjdk:17-slim

# 安装 PostgreSQL
RUN apt update \
    && apt install -y postgresql postgresql-contrib uuid &&  apt install sudo -y

RUN apt install -y libfindbin-libs-perl acl haveged



# 设置 PostgreSQL 用户和数据库
COPY init.sql /

USER root
USER root

# 将 Spring Boot 应用 JAR 文件复制到镜像中
COPY ChatterBox-0.0.1-SNAPSHOT.jar /
COPY readflag /
COPY flag /

RUN chmod 000 /flag


# 编写启动脚本
COPY start.sh /

RUN chmod +x /start.sh

# 指定容器启动时执行的命令
ENTRYPOINT ["/start.sh"]

