FROM ubuntu:latest

WORKDIR /chat_server
COPY chat_server.x86_64 .
COPY chat_server.pck .
COPY libgdsqlite.so .
COPY chat_data.db .


# Create user
RUN addgroup --system g-chat_server
RUN adduser --system u-chat_server --ingroup g-chat_server

RUN chown -R u-chat_server:g-chat_server /chat_server
RUN chmod +x ./chat_server.x86_64

USER u-chat_server:g-chat_server

RUN mkdir -p "/home/u-chat_server/.local/share/godot/app_userdata/Sh3lltris - Chat Server/Datastore/"
RUN mv chat_data.db "/home/u-chat_server/.local/share/godot/app_userdata/Sh3lltris - Chat Server/Datastore/"

EXPOSE 8080

ENTRYPOINT ["./chat_server.x86_64"]


