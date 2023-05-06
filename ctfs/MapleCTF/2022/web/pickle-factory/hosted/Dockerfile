# thanks vie

FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt

COPY . .

EXPOSE 9229

RUN groupadd ctf
RUN useradd -g ctf ctf
RUN chmod 775 /app
USER ctf:ctf

ENTRYPOINT ["python3"]

CMD ["app.py"]
