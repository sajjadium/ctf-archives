FROM gcr.dockerproxy.com/distroless/java11-debian11
COPY ezjna.jar /app.jar
WORKDIR /
CMD ["/app.jar","-Xms1024m","-Xmx1024m"]