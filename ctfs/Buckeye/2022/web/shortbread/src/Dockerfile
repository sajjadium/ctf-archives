FROM python:3.9
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir /app/admin && mkdir /app/admin/logs

COPY app.py ./
COPY static static/
COPY templates templates/
COPY flag.txt /flag.txt

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-k", "eventlet", "--timeout", "500", "--workers", "4", "--access-logfile", "-"]
