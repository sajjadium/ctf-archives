FROM eclipse-temurin:17-jdk
WORKDIR /tmp/compile/
COPY ./ .
RUN ./gradlew --no-daemon bootJar

FROM eclipse-temurin:17-jre
COPY --from=0 /tmp/compile/build/libs/azkaban-escape-0.0.1-SNAPSHOT.jar app.jar
COPY flag.txt flag.txt
CMD ["java", "-jar", "app.jar"]
EXPOSE 8080