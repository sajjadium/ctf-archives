FROM python:3.9.2-slim-buster

RUN pip install flask gunicorn --no-cache-dir

WORKDIR /app
COPY ./ ./

RUN useradd -r -s /usr/sbin/nologin -d /nonexistent app && \
    chmod -R 755 /app && \
    find /app -type f -exec chmod 644 {} \;
RUN python3 db.py && chown -R app:app database

USER app
CMD ["gunicorn", "-w2", "-t4", "--graceful-timeout", "0", "-b0.0.0.0:5000", "app:app"]
