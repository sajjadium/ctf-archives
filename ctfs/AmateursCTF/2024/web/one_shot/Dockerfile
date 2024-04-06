FROM python:3.11
WORKDIR /app

RUN pip install --no-cache-dir Flask gunicorn

COPY app.py flag.txt ./

CMD ["gunicorn", "-b", "[::]:8080", "app:app"]
