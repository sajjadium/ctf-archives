FROM python:3.7

RUN pip install --no-cache-dir gunicorn==19.9.0

COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY app /app

WORKDIR /app

## Add the wait script to the image
COPY wait /wait
RUN chmod +x /wait

## Launch the wait tool and then your application
CMD /wait && /app/start.sh
