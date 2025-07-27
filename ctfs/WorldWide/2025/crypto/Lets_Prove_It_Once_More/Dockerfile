FROM python:3.11

RUN apt update && \
    apt install -y pip wget git && \
    python3 -m pip install --upgrade pip

RUN mkdir /home/ctf
RUN mkdir /home/ctf/logs && chown 65534:65534 /home/ctf/logs
RUN mkdir /home/ctf/utis


COPY requirements.txt /home/ctf/
COPY chall.patch /home/ctf/
WORKDIR /home/ctf/


RUN pip install --requirement /home/ctf/requirements.txt
RUN wget https://cryptohack.org/static/challenges/13431_68413c617b29be47b6e9197b61a5a11a.py
RUN wget https://cryptohack.org/static/listener.py
RUN mv listener.py utis/listener.py
RUN git apply chall.patch

USER 65534:65534

EXPOSE 13431

CMD bash -c "python3 /home/ctf/13431_68413c617b29be47b6e9197b61a5a11a.py"