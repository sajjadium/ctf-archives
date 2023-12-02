FROM tensorflow/tensorflow:2.15.0

RUN useradd -mr counting_stars

WORKDIR /

COPY readflag.c .

RUN gcc readflag.c -o readflag && chown root:root readflag && chmod 4755 readflag

WORKDIR /app

COPY ./requirements.txt .

USER counting_stars

RUN pip install --ignore-installed -r requirements.txt

COPY . .

USER root

RUN chmod -R 777 models

USER counting_stars

CMD python app.py