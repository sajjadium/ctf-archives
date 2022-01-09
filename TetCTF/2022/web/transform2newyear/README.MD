Did you enjoy 2 old school challenges from last year about AMF ?

To help everyone sharpen their skill on Java, this year I continue challenge you with some interesting ideas about pwning Java web-apps. Hope you enjoy all of them !

### NOTE

1) Make sure that your system have installed docker,docker-compose

2) Host Enviroment: 

        latest update on Ubuntu 20.04

3) Network: 

        firewall strictly prohibit making out-going connection

4) You should make sure that your exploit work perfectly on your local env before testing the exploit on the challenge server

5) To make the challenge more stable, our firewall rule only allow 25 req / per second / per client which is enough to solve this challenge and avoid automation scanner

### Setup

chmod +x setup.sh unexpose_docker_port.sh && bash setup.sh


### GLHF