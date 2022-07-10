FROM denoland/deno:1.23.3

EXPOSE 8080

WORKDIR /app

RUN apt update && apt install openssh-client openssl -y

ADD . .
RUN deno cache src/main.ts

RUN chmod +x ./generate.sh && ./generate.sh

CMD ["run", "--allow-net", "--allow-read", "--allow-env", "src/main.ts"]