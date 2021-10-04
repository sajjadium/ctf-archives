FROM python:3.9

WORKDIR /home/user

COPY ./requirements.txt /home/user/

RUN pip install -r requirements.txt

COPY ./src /home/user

CMD ["waitress-serve", "--port=9060", "main:app"]
