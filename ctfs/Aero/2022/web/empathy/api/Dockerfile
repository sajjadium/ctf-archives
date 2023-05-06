FROM python:3.10

RUN useradd --shell /bin/false --no-create-home api

WORKDIR /var/api/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY service .

RUN chmod +x run.sh

USER api

ENTRYPOINT ["./run.sh"]
