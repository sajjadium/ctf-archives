# Setup

How to run the challenge locally:
- `docker compose build`
- `docker compose up`

How to interact the challenge locally:
- `docker ps -a` to show all running containers
- `docker exec -it public-ctf-1 bash` to interact with the container shell


# Your Tasks

I would provide the skeleton code for the exploiting script. 

Your task is to read the hints in the script and complete the script.

# Debug 
You can debug on your container, or you can use mine: 

`docker pull n132/pwn:22.04` (I installed the tools with [this script][1])

After pull-ing the image, you can run the container with this cmd:
`docker run --privileged -it n132/pwn:22.04 zsh`

Then, you shall copy the vulnerable file to the container from the host, whose ID can be found by `docker ps -a`.

Run these commands on your host to perform copy: 

```sh
docker cp ./bin/exp.py {Container ID}:/
docker cp ./bin/chal1 {Container ID}:/
```

Now we can debug the binary on your container by running `python3 exp.py`. Please don't forget to run `tmux` before debugging.

You can also find more cmds on this page: `https://docs.docker.com/engine/reference/commandline/docker/`.

# Debug with GDB

This [article][2] would help you to debug with GDB.



[1]: https://github.com/n132/CTF-Challenges/blob/main/Enviroment/Docker/Ubuntu22.04.sh
[2]: https://n132.github.io/2018/03/06/Debug_With_GDB.html
