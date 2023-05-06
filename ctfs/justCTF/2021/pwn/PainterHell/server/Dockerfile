FROM patryk4815/ctf-tf2server-base:latest

ENV USER tf2
ENV HOME /home/$USER
ENV SERVER /home/$USER/hlserver
USER $USER

# install mods+dependencies
WORKDIR $SERVER/tf2/tf

ENV MM_VERSION 1.12
ENV SM_VERSION 1.11
RUN LATEST_MM=$(wget -q -O - https://mms.alliedmods.net/mmsdrop/$MM_VERSION/mmsource-latest-linux) && \
    LATEST_SM=$(wget -q -O - https://sm.alliedmods.net/smdrop/$SM_VERSION/sourcemod-latest-linux) && \
    wget -O - https://mms.alliedmods.net/mmsdrop/$MM_VERSION/$LATEST_MM | tar -C . -xvz && \
    wget -O - https://sm.alliedmods.net/smdrop/$SM_VERSION/$LATEST_SM | tar -C . -xvz

RUN wget -O tmp.zip http://forums.alliedmods.net/attachment.php?attachmentid=83286 && unzip tmp.zip && rm tmp.zip
RUN wget -O tmp.zip https://builds.limetech.io/files/tf2items-1.6.4-hg279-linux.zip && unzip tmp.zip && rm tmp.zip
RUN wget -O addons/sourcemod/gamedata/tf2.attributes.txt https://raw.githubusercontent.com/FlaminSarge/tf2attributes/master/tf2.attributes.txt
RUN mv addons/sourcemod/plugins/*.smx addons/sourcemod/plugins/disabled/
RUN rm -f -- addons/sourcemod/plugins/*.smx

# install plugins+configs
ADD --chown=tf2:tf2 addons addons

# run
WORKDIR $SERVER
ADD docker-entrypoint.sh .
ENTRYPOINT ["./docker-entrypoint.sh"]
