FROM  openjdk:7u211-jdk-alpine3.9

COPY ./countdown/countdown.jar /countdown.jar

COPY ./countdown/flag ./countdown/readflag /

RUN chown 0:1337 ./flag /readflag && \
    chmod 040 /flag && \
    chmod 2555 /readflag

ENTRYPOINT ["java", "-jar", "/countdown.jar"]

EXPOSE 8084