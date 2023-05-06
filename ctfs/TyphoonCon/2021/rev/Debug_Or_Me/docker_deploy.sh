#!/bin/bash 

# Build the container
sudo docker build --tag max_debugger . || exit 

# Run the container
# DEBUG version for easier debuging
#sudo docker run -d --privileged  --cap-add sys_admin --security-opt apparmor:unconfined -p 2326:2326 -it max_debugger sleep infinity || exit 

sudo docker run -d -p 2326:2326 -it max_debugger sleep infinity || exit 

# DEBUG version -- goes into the container automatically
#docker_ps=$(sudo docker ps -q | head -n1) 
#sudo docker exec -u root -it $docker_ps /bin/bash
