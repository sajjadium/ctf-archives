FROM python:slim

ARG USERNAME=app
ARG DIR=/usr/src/app
WORKDIR ${DIR}
COPY ./challenge.py ./flag.py ./flask_server.py ${DIR}
COPY ./static ${DIR}/static
COPY ./templates ${DIR}/templates

RUN set -eux; \
	pip install flask gunicorn; \
	adduser --disabled-password --no-create-home --gecos ${USERNAME} ${USERNAME}; \
	chmod -R a-wx+Xr ${DIR}

USER ${USERNAME}

EXPOSE 8000

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "flask_server:app" ]
