FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get -y upgrade
RUN apt-get update && apt-get -y install lib32stdc++6 lib32gcc-s1 ca-certificates curl libssl1.1:i386 zlib1g:i386
ADD --chown=root:root flag /flag
RUN chmod 444 /flag
RUN useradd -m game
USER game
RUN mkdir /home/game/Steam
WORKDIR /home/game/Steam
RUN curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
RUN ./steamcmd.sh +force_install_dir /home/game/svends +login anonymous +app_update 276060 validate +exit
RUN mkdir -p /home/game/.steam/sdk32/
RUN ln -s /home/game/Steam/linux32/steamclient.so /home/game/.steam/sdk32/steamclient.so
WORKDIR /home/game/svends
RUN mkdir -p svencoop/addons/metamod/dlls
ADD --chown=game:game metamod.so /home/game/svends/svencoop/addons/metamod/dlls/metamod.so
RUN echo linux addons/note_mm/note_mm.so > svencoop/addons/metamod/plugins.ini
RUN ln -s /home/game/svends/svencoop/dlls/server.so /home/game/svends/svencoop/dlls/hl_i386.so
RUN mkdir svencoop/addons/note_mm
ADD --chown=game:game note_mm.so /home/game/svends/svencoop/addons/note_mm/note_mm.so
CMD ./svends_run -dll addons/metamod/dlls/metamod.so +sv_password $CS_PASSWORD +log on +maxplayers 8 +map stadium4
