FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install build-essential git autoconf xorg-dev libsdl2-dev xvfb x11vnc python
RUN git clone --depth 1 https://github.com/kanjitalk755/macemu.git

WORKDIR /macemu/SheepShaver
RUN make links
WORKDIR /macemu/SheepShaver/src/Unix
RUN ./autogen.sh
RUN make -j8
RUN cp SheepShaver /usr/bin/

WORKDIR /images/
ADD ./ROM /images/ROM
ADD ./papple.dsk /images/root.dsk
RUN mkdir /share
ADD adjust_image.py /images/adjust_image.py
ADD entrypoint.sh /entrypoint.sh

RUN mkdir -p /home/user
RUN groupadd -r user -g 1000
RUN useradd -u 1000 -r -g user \
    -d /home/user/ -c "User" user
RUN chown -R user:user /images/
RUN chown user:user /home/user
RUN chown user:user /share

ENV SDL_RENDER_DRIVER=software
ENV SDL_VIDEODRIVER=x11
EXPOSE 5900

USER 1000
ADD sheepshaver_prefs /home/user/.sheepshaver_prefs
RUN mkdir ~/.vnc
RUN x11vnc -storepasswd tasteless ~/.vnc/passwd

ENTRYPOINT "/entrypoint.sh"

