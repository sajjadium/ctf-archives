The police is investigating a suspicious web forum. They cannot find a way to access it though --- its protected with a password. Luckily, they've managed to set up a packet sniffer between the server and one of its microservices. Unluckily, the traffic is encrypted. Can you help them out?
Connection info:

After starting an instance, use sc to bind it to the port on your machine:

For the web service:

sc -b 5000 <instance_subdomain.instance_domain>

For the packet sniffer:

sc -b 8888 tcp-<instance_subdomain.instance_domain>

You can then connect to the web service on https://localhost:5000 and to the packet sniffer nc localhost 8888. The web server uses a cert signed by the CA in the ca.crt file. It is included for your convenience.
