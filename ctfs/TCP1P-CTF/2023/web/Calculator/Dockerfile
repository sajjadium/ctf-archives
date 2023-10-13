FROM denoland/deno:alpine

WORKDIR /app

COPY . .
RUN deno cache main.js

RUN mv ./flag.txt /flag.txt

EXPOSE 8080

CMD [ "deno", "run", "-A", "--no-prompt", "--unstable", "main.js" ]
