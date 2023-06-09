# docker build -t dot-shortage . && docker run -p 1337:1337 dot-shortage

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y install openjdk-17-jdk-headless socat gcc

RUN adduser --disabled-password --gecos "" user

WORKDIR /home/user/

COPY . .
RUN ./build.sh

# Set the ownership and permissions of the binary and flag file
RUN chown root:root /home/user/build/libs/dot-shortage-all.jar && chown root:root /home/user/flag.txt \
    && chown root:root /home/user/readflag && chmod 400 /home/user/flag.txt && chmod 444 /home/user/build/libs/dot-shortage-all.jar \
    && chmod 4755 /home/user/readflag
EXPOSE 1337
USER user
ENTRYPOINT [ "socat", "-v", "tcp-listen:1337,reuseaddr,fork", "EXEC:'timeout 60 java -jar build/libs/dot-shortage-all.jar'" ]
