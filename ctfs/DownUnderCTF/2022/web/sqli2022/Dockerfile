FROM python:3.10

WORKDIR /app
COPY app.py .

RUN pip3 install flask

ARG FLAG
ENV FLAG=$FLAG

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
