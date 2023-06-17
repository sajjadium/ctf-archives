FROM python:3.11

# Install Chrome
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
  gnupg \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# It won't run from the root user.
RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

# Install redis and dependencies
RUN apt-get -y install redis

RUN chmod 1733 /tmp /var/tmp /dev/shm /proc && \
    chmod go-rx /usr/bin/wall && \
    chmod go-rx /usr/bin/ch* && \
    chmod go-rx /bin/ch*

COPY ./app/ /app/
WORKDIR /app/
RUN pip install -r ./requirements.txt

RUN chown -R root:chrome /app/ && \
    chmod -R 755 /app/

USER chrome
CMD ["python3", "/app/worker.py"]
