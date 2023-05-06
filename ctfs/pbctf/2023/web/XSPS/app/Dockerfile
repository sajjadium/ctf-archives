FROM tiangolo/meinheld-gunicorn-flask:python3.9-2023-02-13

RUN pip install redis

COPY ./app.py /app/main.py
COPY static /app/static/
