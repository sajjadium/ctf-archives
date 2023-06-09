# docker build -t chipmarkt . && docker run -p 8080:8080 chipmarkt
FROM eclipse-temurin:20-jre

RUN adduser --disabled-password --gecos "" user

WORKDIR /home/user/

RUN mkdir user_data

COPY ../../challengeFilesPublic .

RUN chown user:user user_data

EXPOSE 8080
USER user

ENTRYPOINT ["java", "-jar", "-Djava.library.path=.", "backend-all.jar", "./content/"]