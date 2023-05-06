FROM python:3.6
RUN useradd challenge && mkdir /app && pip install flask

WORKDIR /app

COPY . /

RUN chown -R challenge:challenge /app && chown challenge:challenge app.py

USER challenge

RUN mkdir -p /app/wall/image
RUN mkdir -p /app/wall/text
RUN mkdir -p /app/wall/video

CMD python3 app.py