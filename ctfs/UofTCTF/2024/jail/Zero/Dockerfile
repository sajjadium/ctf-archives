FROM python:3.10.13-slim-bullseye

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctfuser

WORKDIR /home/ctfuser/app

COPY --chown=ctfuser:ctfuser chal.py .

RUN echo "uoftctf{fake_flag}" > /home/ctfuser/app/flag && \
    chmod 444 /home/ctfuser/app/flag

RUN chown -R ctfuser:ctfuser /home/ctfuser
EXPOSE 3000

USER root
RUN chmod -R 555 /home/ctfuser/app && \
    chmod 444 /home/ctfuser/app/flag
USER ctfuser

ENTRYPOINT ["socat", "TCP-LISTEN:3000,reuseaddr,fork", "EXEC:'python chal.py',pty,ctty,stderr,raw,echo=0"]
