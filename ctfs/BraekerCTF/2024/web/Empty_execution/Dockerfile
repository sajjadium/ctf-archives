FROM python:alpine3.19

WORKDIR /usr/src/app

RUN pip install flask

COPY empty_execution.py .
RUN chmod 665 ./empty_execution.py

COPY flag.txt .
RUN chmod 664 ./flag.txt

RUN adduser -D ctf 

RUN chown -R root:ctf $(pwd) && \
    chmod -R 650 $(pwd) && \
    chown -R root:ctf /home/ctf/ && \
    chmod -R 650 /home/ctf

RUN mkdir ./executables

USER ctf

EXPOSE 80

CMD ["python", "empty_execution.py"] 