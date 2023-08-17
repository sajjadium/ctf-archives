FROM archlinux:latest

# Note to self: Use docker-compose, you fucking idiot.

# install packages
RUN pacman-key --init && pacman --noconfirm -Sy archlinux-keyring && pacman -Syu --noconfirm firefox python python-pip wget tar -y

# install python-selenium
RUN pip install selenium --break-system-packages

WORKDIR /tmp
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.31.0-linux64.tar.gz && rm geckodriver-v0.31.0-linux64.tar.gz && chmod +x geckodriver && cp geckodriver /usr/local/bin/

COPY firefox-script.py /

CMD bash -c 'python /firefox-script.py'