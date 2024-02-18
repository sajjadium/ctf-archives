FROM denoland/deno:1.40.4

WORKDIR /app

COPY deno.lock server.ts /app/
COPY static/* /app/static/
RUN deno cache --reload --lock=deno.lock server.ts

CMD ["deno", "run", "--lock=deno.lock", "--cached-only", "--allow-read", "--allow-net", "server.ts"]
