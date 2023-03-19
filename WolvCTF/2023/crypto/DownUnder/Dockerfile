FROM debian:bullseye-slim

WORKDIR /usr/src/app

RUN apt-get update                              \
 && DEBIAN_FRONTEND=noninteractive              \
    apt-get install -y --no-install-recommends  \
        python3                                 \
        python3-pip                             \
 && apt-get clean                               \
 && rm -rf /var/lib/apt/lists/*

copy requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 54321

ENV FLASK_APP=key_exchange.py

RUN groupdel staff

ENTRYPOINT [ "./run.sh" ]
