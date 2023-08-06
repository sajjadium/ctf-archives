FROM python:3.7-slim
RUN apt update
RUN apt install python3-pip -y

WORKDIR /usr/src/app/
RUN chmod 775 /usr/src/app/ -R
COPY . .
RUN pip install -r requirement.txt
RUN mv flag.txt / 
RUN groupadd -r swuser -g 433 && \
    useradd -u 431 -r -g swuser -s /sbin/bash -c "swuser" swuser
RUN chown swuser config -R
RUN mkdir public
RUN chown swuser public -R
RUN chmod 444 /flag.txt
USER swuser

CMD [ "python", "app.py" ]


