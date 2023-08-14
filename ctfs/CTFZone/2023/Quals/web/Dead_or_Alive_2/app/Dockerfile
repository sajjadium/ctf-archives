FROM denoland/deno:1.34.1

COPY . /app

RUN chown deno:deno -R /app

WORKDIR /app

USER deno

RUN deno cache app.js

ENTRYPOINT ["deno", "run", "--allow-net", "--allow-read", "--allow-env", "--allow-sys", "app.js"]