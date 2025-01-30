FROM python:3.12-alpine AS builder

RUN apk update --no-cache && apk upgrade --no-cache && apk add socat gmp --no-cache

RUN apk add gcc gmp-dev musl-dev --no-cache && pip install --target=/app fastecdsa

FROM python:3.12-alpine

RUN apk update --no-cache && apk upgrade --no-cache && apk add socat gmp --no-cache

COPY --from=builder /app /app

COPY fast.py /app

WORKDIR /app

ENTRYPOINT socat tcp-l:1337,fork,reuseaddr exec:"python3 /app/fast.py"
