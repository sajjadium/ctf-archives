FROM ubuntu:22.04
RUN apt-get clean && dpkg --add-architecture i386 && apt-get update && apt-get install -y wine wine32 winetricks openjdk-18-jdk
COPY files /files
ENV WINEPREFIX="/wine" WINEDEBUG=-all FLAG=rwctf{NotRealNotRealNotRealNotRealNotReal__flag}
RUN wine wineboot -i && \
	while pgrep wineserver >/dev/null; do echo "Waiting for wineserver"; sleep 1; done \
	&& wine msiexec /i /files/java_card_simulator-3_1_0-u5-win-bin-do-b_70-09_mar_2021.msi && \
	while pgrep wineserver >/dev/null; do echo "Waiting for wineserver"; sleep 1; done \
	&& unzip /files/java_card_tools-win-bin-b_17-06_jul_2021.zip -d /java_card_tools/
ENTRYPOINT bash /files/entrypoint.sh
