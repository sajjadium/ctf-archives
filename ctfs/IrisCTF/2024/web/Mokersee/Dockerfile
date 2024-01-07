FROM python:3.11.1

RUN /usr/sbin/useradd -u 1000 user

RUN python3 -m pip install flask gunicorn numpy pillow scikit-image
RUN apt-get update
RUN apt-get install -y socat

COPY chal.py /home/user/
COPY run.sh /home/user/
COPY style.css /home/user/
COPY templates /home/user/templates
COPY images /home/user/images

CMD /home/user/run.sh
