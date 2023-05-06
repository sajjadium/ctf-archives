FROM openjdk:18-slim-bullseye

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# create user
RUN groupadd chalusr
RUN useradd -ms /bin/bash -g chalusr chalusr

COPY spoink/target/spoink-0.0.1-SNAPSHOT-spring-boot.jar ./
COPY spoink/public ./public
COPY spoink/templates ./templates
COPY getflag ./

RUN chmod 111 ./getflag

USER chalusr
CMD ["java", "-jar", "/usr/src/app/spoink-0.0.1-SNAPSHOT-spring-boot.jar"]