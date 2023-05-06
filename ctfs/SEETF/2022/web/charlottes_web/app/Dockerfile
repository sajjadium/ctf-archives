FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app/

ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:80", "app:app"]