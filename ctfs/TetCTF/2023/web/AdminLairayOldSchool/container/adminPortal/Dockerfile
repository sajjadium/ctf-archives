FROM ubuntu:20.04

USER root
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y nginx supervisor unzip wget curl

# INSTALL JDK
ENV JDK_VERSION jdk-7u80
ENV BUILD_VERSION 03
WORKDIR /tmp
RUN \
  curl -s -L -o $JDK_VERSION.tgz https://files-cdn.liferay.com/mirrors/download.oracle.com/otn-pub/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz && \
  mkdir -p /opt/jdk/$JDK_VERSION && \
  tar -zxf $JDK_VERSION.tgz -C /opt/jdk/$JDK_VERSION --strip-components 1 && \
  rm $JDK_VERSION.tgz && \
  update-alternatives --install /usr/bin/java java /opt/jdk/$JDK_VERSION/bin/java 100 && \
  update-alternatives --install /usr/bin/javac javac /opt/jdk/$JDK_VERSION/bin/javac 100 && \
  update-alternatives --install /usr/bin/jar jar /opt/jdk/$JDK_VERSION/bin/jar 100


# GET LIFERAY
RUN useradd -ms /bin/bash liferay
ADD http://downloads.sourceforge.net/project/lportal/Liferay%20Portal/6.1.2%20GA3/liferay-portal-tomcat-6.1.2-ce-ga3-20130816114619181.zip /tmp/liferay-portal-tomcat-6.1.2-ce-ga3-20130816114619181.zip

RUN unzip /tmp/liferay-portal-tomcat-6.1.2-ce-ga3-20130816114619181.zip -d /opt
RUN rm -f /tmp/liferay-portal-tomcat-6.1.2-ce-ga3-20130816114619181.zip

# setup supervisor
COPY ./container/adminPortal/supervisor.conf /etc/supervisor.conf

RUN rm /etc/nginx/sites-available/default && rm /etc/nginx/sites-enabled/default
COPY ./container/adminPortal/default /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

COPY ./container/adminPortal/flag.txt ./container/adminPortal/readflag /
RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag


RUN chown -R liferay:liferay /opt/liferay-portal-6.1.2-ce-ga3

ENTRYPOINT ["supervisord", "-c", "/etc/supervisor.conf"]

EXPOSE 80