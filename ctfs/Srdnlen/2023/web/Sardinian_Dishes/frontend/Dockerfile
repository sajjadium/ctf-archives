FROM python:3

COPY src/ /home
RUN pip3 install flask
RUN pip3 install pyratemp
RUN pip3 install requests
CMD [ "python3", "/home/app.py" ]
