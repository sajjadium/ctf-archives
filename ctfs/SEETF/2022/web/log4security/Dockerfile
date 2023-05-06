FROM openjdk:11 as builder

WORKDIR /app

COPY ./log4security/.mvn /app/.mvn
COPY ./log4security/mvnw /app/mvnw
COPY ./log4security/pom.xml /app/pom.xml
RUN ["./mvnw", "verify", "clean", "--fail-never"]

COPY ./log4security/. /app
RUN ["./mvnw", "package"]

FROM openjdk:11

RUN addgroup spring && adduser spring --ingroup spring
USER spring:spring

COPY --from=builder /app/target /build

WORKDIR /build

ENTRYPOINT ["java", "-jar", "log4security-0.0.1-SNAPSHOT.jar"]