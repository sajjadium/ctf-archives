FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
  POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi --no-root \
  && apt update \
  && apt install -y --no-install-recommends wait-for-it \
  && rm -rf /var/lib/apt/lists/*


COPY . .

EXPOSE 8000

CMD  ["fastapi", "run", "./mvmcryption/app.py"]
