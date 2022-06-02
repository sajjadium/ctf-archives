FROM python
RUN apt-get update && apt-get install --fix-missing -y locales python3-pip python3-dev build-essential git

ADD ./app /app/
WORKDIR /app/

RUN pip3 install -r /app/requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]