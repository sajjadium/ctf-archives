FROM python:3.9-alpine

RUN apk update
RUN apk add zip gcc libc-dev g++
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn==20.1.0

COPY app /app

## Add the wait script to the image
COPY wait /wait
RUN chmod +x /wait

## Launch the wait tool and then your application
## wait is not important for this task. It is just a lazy way to wait until the database fully started
CMD /wait && /app/start.sh
