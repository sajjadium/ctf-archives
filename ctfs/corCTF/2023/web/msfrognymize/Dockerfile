FROM python:3.9

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    redis-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY . /app

RUN mv flag.txt /

EXPOSE 4444

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
