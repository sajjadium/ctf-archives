FROM python:3.10-slim-bullseye


LABEL auther_template="khanhhnahk1"


RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update 

# install flask
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    flask

# Copy the source code and startup script to the root directory
COPY ./src/ /app
COPY ./service/docker-entrypoint.sh /

# expose port
EXPOSE 8080
RUN groupadd -r thru_the_filter && useradd -r -g thru_the_filter thru_the_filter
RUN echo "ISITDTU{test_flag}"> /app/flag.txt
RUN chmod 440 /app/flag.txt
RUN chown -R root:thru_the_filter /app


USER thru_the_filter

WORKDIR /app


ENTRYPOINT ["/bin/bash","/docker-entrypoint.sh"]