FROM python:3.7-buster

RUN apt-get update -yqq && apt-get install -y \
    lib32z1 xinetd \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade --no-cache-dir rctf-golf

RUN useradd -m ctf

WORKDIR /

COPY ./ctf.xinetd /etc/xinetd.d/ctf

COPY ./start.sh /start.sh
COPY ./limit.py /limit.py
COPY ./kevin-higgs.sh /kevin-higgs.sh
COPY ./kevin-higgs /kevin-higgs
COPY ./flag.txt /flag.txt

RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

RUN chown root:ctf /start.sh /limit.py /kevin-higgs /kevin-higgs.sh /flag.txt&& \
    chmod 750 /start.sh /limit.py /kevin-higgs /kevin-higgs.sh && \
    chmod 740 /flag.txt

CMD ["/start.sh"]

EXPOSE 9999
