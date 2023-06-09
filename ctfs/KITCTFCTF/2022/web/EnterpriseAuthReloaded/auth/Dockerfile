FROM denoland/deno:alpine

EXPOSE 8000

WORKDIR /app
USER deno

ADD . .
RUN deno cache server.ts

CMD ["run", "--allow-net", "--allow-env", "server.ts"]
