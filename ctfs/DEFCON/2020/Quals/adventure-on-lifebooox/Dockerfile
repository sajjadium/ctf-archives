from ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

# example:
RUN apt-get -qq update && apt-get install -qq --no-install-recommends xinetd rsyslog python3.8 x11vnc xvfb tinywm openbox xdotool wmctrl x11-utils xterm golly

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 && \
    echo 0|update-alternatives --config python3

RUN apt-get install -qq python-dev python3-pip python3.8-dev netcat xserver-xephyr vnc4server scrot redis-server supervisor

# FAKE FLAG
ARG THE_FLAG="OOO{THiS_iS_NoT_a_DRoiD_oR_a_FLaG}"
run touch /flag && chmod 644 /flag && echo $THE_FLAG > /flag

RUN pip3 install pillow pyvirtualdisplay pyscreenshot entrypoint2 redis rq

RUN useradd -s /bin/bash -m rrx

COPY src/.golly /home/rrx/.golly
COPY service.conf /etc/xinetd.d/lifeboxserv
COPY supervisord.conf /etc/supervisord.conf

COPY banner_fail /banner_fail

COPY src/adventure_lifebooox.mc /

COPY src/lifebox-run.py /
COPY src/__init__.py /
COPY src/gamerunner.py /
COPY src/lifebox_task.py /
COPY src/workers.py /

RUN chmod +x /*.py

ENV GOL_WORKERS=5

RUN echo "" > /var/log/lifeworkers_stdout.log && chown rrx:rrx /var/log/lifeworkers_stdout.log
RUN echo "" > /var/log/lifeworkers_stderr.log && chown rrx:rrx /var/log/lifeworkers_stderr.log

EXPOSE 37451

CMD ["/usr/bin/supervisord","-c","/etc/supervisord.conf"]
