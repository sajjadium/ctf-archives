FROM maven:3.8.3-openjdk-17 as buildstage
COPY pom.xml ./
RUN mvn -B -f pom.xml dependency:go-offline
COPY . .
RUN mvn -B install

FROM openjdk:17
COPY --from=buildstage ./target/springbrut-0.0.1-SNAPSHOT.jar ./springbrut.jar
COPY flag /flag
CMD [ "java", "-XX:+UseZGC", "-jar",  "springbrut.jar"]
EXPOSE 8080