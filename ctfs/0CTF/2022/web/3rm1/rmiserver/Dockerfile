FROM openjdk:8u201-alpine


RUN addgroup -S ctfgroup && adduser -S ctf -G ctfgroup 
RUN mkdir /opt/app

COPY threermiserver.jar /opt/app

WORKDIR /opt/app

USER ctf
CMD ["java", "-jar", "/opt/app/threermiserver.jar"]
