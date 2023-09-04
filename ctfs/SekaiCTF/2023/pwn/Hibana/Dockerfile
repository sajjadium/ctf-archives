FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install lib32stdc++6 lib32gcc-s1 ca-certificates curl zlib1g:i386
RUN curl http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_i386.deb -O && dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_i386.deb && rm libssl1.1_1.1.1f-1ubuntu2.19_i386.deb
RUN useradd -m steam
USER steam
RUN mkdir /home/steam/Steam
WORKDIR /home/steam/Steam
RUN curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
RUN ./steamcmd.sh +force_install_dir /home/steam/svends +login anonymous +app_update 276060 +exit || true
RUN mkdir -p /home/steam/.steam/sdk32/
RUN ln -s /home/steam/Steam/linux32/steamclient.so /home/steam/.steam/sdk32/steamclient.so
WORKDIR /home/steam/svends
CMD ./svends_run -dll addons/metamod/dlls/metamod.so -norestart -insecure -port 27015 +maxplayers 3 +sv_password $PASSWORD +sv_spectator_password $PASSWORD +log off +map stadium4
