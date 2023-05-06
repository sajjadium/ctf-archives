# IMAGE 2: run challenge
# @AUTHOR: feel free to change base image as necessary (i.e. python, node)
FROM ubuntu:18.04

# @AUTHOR: run requirements here
RUN apt-get -qq update && apt-get -qq --no-install-recommends install xinetd python3 python3-pip
RUN python3 -m pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# copy source files
WORKDIR /chal

# Docker wont do globbing properly, so each file goes in on it's own
COPY src/app.py /chal/
COPY src/check.py /chal/
COPY src/filters.py /chal/
# COPY src/limit.py /chal/

RUN mkdir /chal/templates
COPY src/templates/index.html /chal/templates/
COPY src/templates/secure_translate.html /chal/templates/
# RUN ls -lahR /chal

# copy flag
COPY flag /flag

# make user
RUN useradd chal

# copy service info
# COPY container_src/* /

# Set perms
RUN chown -R root:root /chal/*
RUN chmod -R o-w /chal/*
RUN chown -R root:root /flag
RUN chmod -R o-w /flag


# run challenge
EXPOSE 30069
# RUN chmod +x /run_chal.sh
USER chal
CMD ["python3", "/chal/app.py"]
