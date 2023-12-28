FROM ubuntu:23.10 as base


RUN apt-get update && apt-get install --yes iproute2 ca-certificates curl gnupg python3-pip &&\
install -m 0755 -d /etc/apt/keyrings &&\
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg &&\
chmod a+r /etc/apt/keyrings/docker.gpg &&\
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null &&\
apt-get update &&\
apt-get install --yes docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin &&\
apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app
COPY interface/requirements.txt .
RUN pip install --break-system-packages -r requirements.txt
COPY interface interface
COPY cookmaster-bin cookmaster
WORKDIR /app/interface

FROM base as develop
CMD uvicorn main:app --reload --host 0.0.0.0 --port 31337

FROM base as production
RUN pip install --break-system-packages gunicorn
CMD gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:31337

FROM base as cleanup
CMD python3 ./cleanup.py
