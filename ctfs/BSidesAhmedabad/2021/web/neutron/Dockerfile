FROM ubuntu:focal

COPY ./neutron-app_1.0.0_amd64.deb /tmp/neutron.deb
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y curl tightvncserver icewm
RUN apt -y install /tmp/neutron.deb

COPY ./flag.txt /flag.txt
RUN chmod 400 /flag.txt

COPY ./read_flag /read_flag
RUN chmod 4555 /read_flag

RUN useradd -ms /bin/bash ctf
USER ctf

ENV USER=ctf
ENV HOME=/home/ctf

RUN mkdir $HOME/.vnc/
RUN /bin/bash -c 'vncpasswd -f <<<"hunter0" >"$HOME/.vnc/passwd" && chmod 600 $HOME/.vnc/passwd'
RUN echo 'icewm&' > "$HOME/.vnc/xstartup" && chmod +x $HOME/.vnc/xstartup

CMD /bin/sh -c 'vncserver :10 && DISPLAY=:10 neutron-app'