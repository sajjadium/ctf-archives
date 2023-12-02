FROM openjdk:15.0.2

COPY java.security ${JAVA_HOME}/conf/security/
COPY readflag /readflag
RUN chmod 600 /flag
RUN chmod +x /readflag
RUN chmod u+s /readflag

RUN mkdir /opt/app
WORKDIR /opt/app
COPY babyrasp.jar ./
COPY art_galery.jar ./
COPY ./heavy_images ./

USER nobody
CMD ["java", "-javaagent:babyrasp.jar" ,  "-jar", "art_galery.jar", "--server.port=80"]