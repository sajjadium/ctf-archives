FROM python:3

WORKDIR /secret_of_j4ck4l

COPY app.py /secret_of_j4ck4l/app.py
COPY message /secret_of_j4ck4l/message
COPY flag.txt /secret_of_j4ck4l/flag.txt


RUN apt-get update  \
    && useradd -m ctf-player \
    && chown -R ctf-player /secret_of_j4ck4l

USER ctf-player

RUN pip install Flask

EXPOSE 4053

CMD ["python3", "app.py"]