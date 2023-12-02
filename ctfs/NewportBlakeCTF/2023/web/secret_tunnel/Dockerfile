FROM python:3.10-slim AS app

WORKDIR /chall

RUN pip3 install flask requests

COPY . .
RUN chmod 777 ./run.sh

CMD ["sh", "-c", "python3 -m flask --app flag.py run --host=0.0.0.0 --port=1337 & python3 -m flask --app main.py run --host=0.0.0.0"]
