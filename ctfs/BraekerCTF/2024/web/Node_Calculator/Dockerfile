FROM tomcat:jre11

RUN rm -rf /usr/local/tomcat/webapps/* ; \
    rm -rf /usr/local/tomcat/work/Catalina/localhost/* ; \
    rm -rf /usr/local/tomcat/conf/Catalina/localhost/*

RUN chmod -R 400 /usr/local/tomcat/conf

ADD NodeCalculator.war /usr/local/tomcat/webapps/

COPY ./flag.txt /tmp/
COPY ./location.txt /tmp/

EXPOSE 8080

CMD ["catalina.sh", "run"]