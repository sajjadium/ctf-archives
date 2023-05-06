Connect to the server to see your friends and get a "guest" key!! You'll then be able to test your client by talking with the echo-bot (you'll need to establish a session key through the server first). Don't worry about the other users, they won't even talk to you unless you're their friend!

server - nc rar.chal.cybears.io 9000

clients - nc rar.chal.cybears.io [ports_provided_by_server]

using the provided client_initiator - python3 client_initiator.py -s rar.chal.cybears.io -p 9000 -t rar.chal.cybears.io -q [echo_bot_port]
