FROM python:3.9


WORKDIR /app
COPY . /app


RUN set -eux; \
	\
	apt update; \
	pip install -r requirements.txt; \
	adduser --disabled-password --gecos "" --home /home/app --shell /bin/bash app; \
    	chown -R app:app /home/app /app;

USER app
ENV HOME /home/app

EXPOSE 5000
CMD ["gunicorn", "--keep-alive", "10", "-k", "gevent", "--bind", "0.0.0.0:5000", "-w", "2", "app:app"]
