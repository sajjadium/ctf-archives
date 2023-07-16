FROM python:3.10-slim-buster

RUN pip3 install flask
COPY flag.txt /

WORKDIR /app
COPY app/* /app/
copy app/templates/* /app/templates/
copy app/themes/* /app/themes/

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]