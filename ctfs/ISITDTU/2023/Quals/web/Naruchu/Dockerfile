FROM python:slim AS app

RUN useradd -m onsra

USER onsra
WORKDIR /home/onsra

COPY --chown=onsra:onsra requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=onsra:onsra server.py .

RUN rm .bash_logout .bashrc .profile

COPY --chown=onsra:onsra flag.txt .

RUN find ./ -type f -exec chmod 400 {} \;
RUN find ./ -type d -exec chmod 500 {} \;


ENV DEPLOY_ENV=ISITDTU
EXPOSE 11111
CMD python3 server.py
