FROM python:3.10-alpine

COPY ./src /app
WORKDIR /app
RUN mkdir /app/uploads/admin
RUN mkdir /app/static/uploads/admin
COPY test-flag.png /
COPY file_remover.py /tmp
COPY run.sh /tmp
RUN pip install flask requests imageio
RUN chmod +x /tmp/run.sh

EXPOSE 9999

CMD ["/tmp/run.sh"]