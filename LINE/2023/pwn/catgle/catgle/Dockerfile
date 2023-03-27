FROM ubuntu:22.04

RUN groupadd -g 1000 catgle
RUN useradd -g catgle -s /bin/bash catgle

RUN apt-get update
RUN apt-get install -y python3-pip libmysqlclient-dev

COPY ./ /app
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chown root:root -R /app
RUN chmod 777 /app/uploads

USER catgle

CMD /bin/bash -c "gunicorn --bind 0:4444 main:app --worker-class uvicorn.workers.UvicornWorker --user catgle --group catgle"
