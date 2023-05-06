FROM tomcat:8.5.87-jdk8-temurin-focal

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

COPY ./target/demo-1.0-SNAPSHOT.war ./webapps/demo.war
ADD ./lib/* ./lib/
ADD ./conf/* ./conf/

CMD ["catalina.sh", "run"]