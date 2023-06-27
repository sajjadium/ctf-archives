FROM python:3-alpine

RUN set -eux; \
    apk add --no-cache socat;

# Copy application source
WORKDIR /app
COPY lost_basis.py .

# Set non-root user
RUN adduser "--disabled-password"  user
USER user

# Set port
EXPOSE 3535

CMD ["socat", "TCP-LISTEN:3535,reuseaddr,fork", "EXEC:'python /app/lost_basis.py'"]