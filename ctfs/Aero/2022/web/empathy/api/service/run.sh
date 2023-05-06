#!/bin/sh

exec uvicorn \
    --host 0.0.0.0 \
    --port 8080 \
    --workers 4 \
    --forwarded-allow-ips '*' \
    -- \
    app:app
