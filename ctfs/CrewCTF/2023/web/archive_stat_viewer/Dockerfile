FROM tiangolo/meinheld-gunicorn-flask:latest

RUN pip install flask

RUN groupadd -r user -g 1000 && useradd -r -g 1000 -u 1000 user

COPY ./web-apps /web-apps

WORKDIR /web-apps/src/

RUN chmod -R 550 .
RUN chown -R root:user .

EXPOSE 1337

CMD gunicorn --user user --group user --bind :8080 main:app
