FROM python:slim AS app

RUN useradd -m ctf

USER ctf
WORKDIR /home/ctf

COPY --chown=ctf:ctf requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=ctf:ctf server.py .

RUN rm .bash_logout .bashrc .profile

COPY --chown=ctf:ctf flag.txt .

RUN find ./ -type f -exec chmod 400 {} \;
RUN find ./ -type d -exec chmod 500 {} \;

ENV DEPLOY_ENV=production
EXPOSE 5000
CMD python3 server.py
