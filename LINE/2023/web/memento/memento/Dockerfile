FROM eclipse-temurin:17.0.6_10-jdk AS TEMP_BUILD_IMAGE

ARG DEST=/usr/src/app
WORKDIR ${DEST}

COPY *.gradle gradle.* gradlew ./
COPY gradle/ ./gradle/
RUN ./gradlew build -x test --parallel --continue > /dev/null 2>&1 || true
COPY src src
RUN ./gradlew bootJar


FROM eclipse-temurin:17.0.6_10-jre

ARG DEST=/usr/src/app
WORKDIR /usr/app/

RUN addgroup spring && adduser --ingroup spring spring
USER spring:spring

COPY --from=TEMP_BUILD_IMAGE ${DEST}/build/libs/*.jar app.jar
ADD start.sh .

ENTRYPOINT ["sh", "start.sh"]