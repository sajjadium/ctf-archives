FROM python:3.10.5-bullseye

RUN useradd -m ctf

WORKDIR /home/ctf

RUN apt-get update && \
    apt-get install -y lib32z1 xinetd && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Connection banned." > /etc/banner_fail

RUN pip3 install requests tensorflow numpy matplotlib h5py scikit-image keras

ADD images ./images
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY challenge_model.h5 server.py start.sh ./

RUN chmod +x /home/ctf/start.sh && \
    chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf

ENV PYTHONUNBUFFERED=1

CMD ["/home/ctf/start.sh"]

EXPOSE 10105

# docker build --tag ottercat .
# docker run -d --publish 10105:10105 --name ottercat ottercat