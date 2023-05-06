FROM python:3.8.5

COPY ./src/app /app

WORKDIR /app
RUN pip install pipenv &&\
    pipenv install --system

RUN adduser app && chown -R app /app

ENTRYPOINT [ "uwsgi", "--ini", "/app/uwsgi.ini"]