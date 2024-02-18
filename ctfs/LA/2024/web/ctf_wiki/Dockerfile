FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
COPY app.py setup.sql /app/
COPY templates /app/templates
COPY static /app/static

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:1337", "app:app"]
