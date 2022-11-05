all: server1 flag_client

server1: server/server.c
	gcc -O3 -o server/server server/server.c

flag_client: flag-client/client.c 
	gcc -O3 -o flag-client/flag_client flag-client/client.c

