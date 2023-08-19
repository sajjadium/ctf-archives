FROM python:3

RUN pip install flask gunicorn gevent
RUN pip install pycryptodome

RUN useradd -s /sbin/nologin app
COPY . /home/app

USER app

WORKDIR /home/app

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "-w", "4", "--timeout=10", "-k", "gevent"]
