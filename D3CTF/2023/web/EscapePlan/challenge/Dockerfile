FROM python:3.8-alpine
RUN apk add --no-cache gcc musl-dev linux-headers shadow
WORKDIR /code
RUN groupadd -r flask && useradd -r -g flask flask && chown -R flask:flask /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY readflag /readflag
COPY flag /flag
RUN chmod 700 /flag
COPY readflag /readflag
RUN chmod +s /readflag
USER flask
CMD ["flask", "run"]
