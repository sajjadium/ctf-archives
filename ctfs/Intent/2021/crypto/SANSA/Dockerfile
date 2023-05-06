FROM python:3.9.7

WORKDIR /usr/src/app
COPY . .


RUN set -eux; \
    \
    pip install gunicorn; \
    pip install -r requirements.txt; \
    useradd -c app -m -d /home/app -s /bin/bash app; \
    chown -R app:app /home/app

USER app
ENV HOME /home/app

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "--limit-request-line", "0", "-w", "2", "index:app" ]
