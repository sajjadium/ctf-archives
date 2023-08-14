FROM continuumio/miniconda3

RUN pip3 install pycryptodome numpy galois

COPY ./src /app
WORKDIR /app

CMD ["python3","/app/main.py"]