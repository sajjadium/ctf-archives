FROM ubuntu:20.04

RUN apt-get -y update && apt-get -y install software-properties-common

RUN apt-get install -y openjdk-11-jdk

RUN apt-get -y install wget
RUN mkdir /usr/local/tomcat
RUN wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.75/bin/apache-tomcat-8.5.75.tar.gz -O /tmp/tomcat.tar.gz
RUN cd /tmp && tar xvfz tomcat.tar.gz
RUN cp -Rv /tmp/apache-tomcat-8.5.75/* /usr/local/tomcat/
RUN rm -rf /tmp/* && rm -rf /usr/local/tomcat/webapps/

COPY src/ROOT/ /usr/local/tomcat/webapps/ROOT/
COPY flag /flag
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

