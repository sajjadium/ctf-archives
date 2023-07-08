ARG DENO_VERSION=1.32.3

FROM denoland/deno:bin-$DENO_VERSION AS deno
FROM ubuntu
COPY --from=deno /deno /usr/local/bin/deno

RUN useradd app

WORKDIR /home/app

COPY src/ /home/app

RUN chmod a+x /home/app/run.sh
RUN chmod a+rw /home/app

EXPOSE 8080

# safe-proxy-flag-provider is exposed on internal network
ENV PROVIDER_HOST="safe-proxy-flag-provider:8082"
ENV PROVIDER_TOKEN=REDACTED

USER app

CMD /home/app/run.sh
