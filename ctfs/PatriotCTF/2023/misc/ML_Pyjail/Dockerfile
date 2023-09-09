FROM ubuntu:20.04

RUN apt-get -y update --fix-missing && apt-get -y upgrade

RUN apt-get -y install socat python3 python3-pip

RUN groupadd -r pctf && useradd -r -g pctf pctf

WORKDIR /home/pctf

RUN chown pctf:root . -R

COPY MLjail/requirements.txt /home/pctf/MLjail/requirements.txt

RUN pip3 install --no-cache-dir -r /home/pctf/MLjail/requirements.txt

RUN [ "python3", "-c", "import nltk; nltk.download('punkt', download_dir='/home/pctf/nltk_data')" ]

RUN python3 -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data')"

ENV NLTK_DATA=/usr/local/share/nltk_data

USER pctf

CMD ["./entrypoint.sh"]