FROM openjdk:8 as jdk_env

FROM gcc:8  as compile_env
COPY ./readflag.c /tmp
RUN cd /tmp &&  gcc readflag.c -o readflag
FROM ubuntu

ENV DRUID_VERSION="25.0.0" \
    JAVA_HOME="/opt/jdk"

COPY --from=jdk_env /usr/local/openjdk-8/ /opt/jdk
COPY --from=compile_env /tmp/readflag /readflag
COPY ./flag /flag

RUN set -ex && \
    apt update && apt install -y wget libfindbin-libs-perl acl haveged && \
    cd /opt &&\
    wget https://dlcdn.apache.org/druid/${DRUID_VERSION}/apache-druid-${DRUID_VERSION}-bin.tar.gz && \
    tar xf apache-druid-${DRUID_VERSION}-bin.tar.gz && \
    mv apache-druid-${DRUID_VERSION} druid && rm apache-druid-${DRUID_VERSION}-bin.tar.gz 

WORKDIR /opt/druid

RUN groupadd ctf && useradd -g ctf ctf && \
    mkdir /opt/druid/log/ /opt/druid/var/ && \
    chgrp -R ctf /opt/druid  && \
    chmod u=srx,g=rx,o=rx /readflag && \
    chmod g+w log/ var/ && \
    setfacl -d -m group:ctf:rwx ./log ./var ./lib ./extensions ./conf  &&\
    chmod ug+x ./bin/* &&\
    chmod 400 /flag && \
    rm -rf /var/lib/apt/lists/* 

EXPOSE 8888

CMD ["su","ctf","-c","./bin/start-micro-quickstart"]
