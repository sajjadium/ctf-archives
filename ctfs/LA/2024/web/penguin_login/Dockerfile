FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
COPY app.py flag.txt /app/

ENV PORT=8080
CMD ["gunicorn", "-w", "1", "app:app"]
