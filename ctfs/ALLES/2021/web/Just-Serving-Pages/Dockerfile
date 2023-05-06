FROM maven:3.6.1-jdk-8 as maven_builder
WORKDIR /app
COPY src /app
WORKDIR /app/
RUN ls -al
RUN ["/usr/local/bin/mvn-entrypoint.sh", "mvn", "package"]

FROM tomcat:8.5.43-jdk8
RUN rm -rf /usr/local/tomcat/webapps/ROOT
COPY --from=maven_builder /app/target/just-serving-pages-1.0.0-SNAPSHOT.war /usr/local/tomcat/webapps/ROOT.war
RUN sed -i 's/port="8080"/port="1024"/' ${CATALINA_HOME}/conf/server.xml
COPY flag /flag