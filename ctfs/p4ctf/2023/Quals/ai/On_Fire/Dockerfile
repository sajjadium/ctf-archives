FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3.10 curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python3.10 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["gunicorn", "--conf", "app/gunicorn_conf.py", "--bind", "0.0.0.0:8000", "app.main:app"]
