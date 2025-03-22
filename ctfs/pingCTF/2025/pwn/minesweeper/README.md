Author: lexu Flag format: ping{.*} Description:

This challange is quite cpu intensive, so launch your instance only when submitting the flag. Launch local instance with the following command:

docker-compose up

Also by defualt, client will connect to localhost:30420 which is the default port of the server when running using docker-compose up. If you want to connect to a different server, you can set the IP_ADDRESS and PORT in client code inside main_controller.gd file.

Note: dockerized challenges will be available few hours after start of CTF to decrease load on out infrastructure at start
