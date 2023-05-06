FROM python:3.8.16-slim-bullseye

RUN useradd ctf

COPY flag.txt start.sh /

# setup app

WORKDIR /app

COPY app /app/

RUN pip install -r requirements.txt

# setup nginx

RUN apt update -y && apt install -y nginx

COPY nginx.conf /etc/nginx/nginx.conf

# start services
EXPOSE 1337

CMD nginx -g "daemon off;" & (su ctf && python3 app.py --workers=16)


