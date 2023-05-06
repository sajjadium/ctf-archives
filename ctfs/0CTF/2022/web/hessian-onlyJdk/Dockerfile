FROM openjdk:8u342-slim


RUN adduser ctf && addgroup ctfgroup && adduser ctf ctfgroup
RUN mkdir /opt/app

COPY hessian-onlyJdk.jar /opt/app
COPY JavaUtils.class /opt/app
COPY jvmtiagent.so /opt/app
COPY flag /flag

WORKDIR /opt/app

USER ctf
CMD ["java", "-agentpath:/opt/app/jvmtiagent.so=/opt/app/JavaUtils.class", "-jar", "/opt/app/hessian-onlyJdk.jar"]
