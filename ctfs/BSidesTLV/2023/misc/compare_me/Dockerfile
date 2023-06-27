FROM python:3-alpine as builder
WORKDIR /build

RUN set -eux; \
    apk add --no-cache build-base;

COPY memcmp_all.c .
RUN gcc -shared memcmp_all.c -o memcmp_all.so

FROM python:3-alpine

RUN set -eux; \
    apk add --no-cache socat;

# Copy application source
WORKDIR /app
COPY compare_me.py .
COPY --from=builder /build/memcmp_all.so /app/memcmp_all.so

# Set non-root user
RUN adduser "--disabled-password"  user
USER user

# Set port
EXPOSE 3535

CMD ["socat", "TCP-LISTEN:3535,reuseaddr,fork", "EXEC:'python /app/compare_me.py'"]
