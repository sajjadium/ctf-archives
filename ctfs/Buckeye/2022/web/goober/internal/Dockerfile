FROM python:3.10-rc-bullseye

RUN python -m pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

ENV PORT=5001
EXPOSE 5001

CMD gunicorn -k gthread app:app