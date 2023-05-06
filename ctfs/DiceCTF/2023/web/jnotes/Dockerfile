FROM openjdk:17-slim-bullseye

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# create user
RUN groupadd chalusr
RUN useradd -ms /bin/bash -g chalusr chalusr

COPY jnotes/target/app.jar ./

USER chalusr
CMD ["java", "-jar", "/usr/src/app/app.jar"]