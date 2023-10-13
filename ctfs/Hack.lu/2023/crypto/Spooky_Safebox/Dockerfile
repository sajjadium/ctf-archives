FROM python:3.11-alpine

RUN pip install pipenv \
    && apk add socat

WORKDIR /app
ADD Pipfile /app/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
ADD app.py /app/
ADD cryptod.py /app/
ADD proofofwork.py /app/

CMD ["socat", "tcp-listen:5566,fork,reuseaddr", "system:pipenv run python3 app.py"]
