FROM debian:stable-slim
RUN apt-get update
RUN apt-get install nano apt-utils -y
RUN apt-get upgrade -y
RUN apt-get install curl python3 python3-pip gunicorn3 nginx xvfb -y
COPY nginx.conf /etc/nginx/nginx.conf
RUN useradd ctf

RUN pip3 install flask requests selenium pyvirtualdisplay flask_hcaptcha

RUN apt-get install wget unzip -y && \
	wget https://chromedriver.storage.googleapis.com/95.0.4638.54/chromedriver_linux64.zip && \
	unzip chromedriver_linux64.zip && \
	mv chromedriver /usr/bin/chromedriver

RUN echo 'deb http://download.opensuse.org/repositories/home:/ungoogled_chromium/Debian_Bullseye/ /' | tee /etc/apt/sources.list.d/home-ungoogled_chromium.list > /dev/null
RUN curl -s 'https://download.opensuse.org/repositories/home:/ungoogled_chromium/Debian_Bullseye/Release.key' | gpg --dearmor | tee /etc/apt/trusted.gpg.d/home-ungoogled_chromium.gpg > /dev/null
RUN apt update
RUN apt install -y ungoogled-chromium

COPY ./start.sh /start.sh
RUN chmod 555 /start.sh
RUN chown root:root start.sh

COPY files/ /chall
RUN chmod -R 555 /chall
RUN chown -R root:root /chall

COPY bot/ /bot
# RUN mv /bot/chromedriver /usr/bin/chromedriver
RUN chmod -R 555 /bot
RUN chown -R ctf:ctf /bot

ENTRYPOINT /start.sh
