Will you be able to corrupt some politicians to grab the flag? \n Note: try running the exploit multiple times IMPORTANT NOTE: build your exploit and test it locally using the given docker image, everythin you need is already packed there. Only when you are 90% sure that the exploit works run it on the challenge service. There is just one copy of the challenge running that resets itself every 20 seconds for costs reduction so please be respectful.


# Build

`docker build -t myasnik/every-italian-politician:v1-dbg .`

# Run

`docker run -it -p 8080:80 myasnik/every-italian-politician:v1-dbg`

Inside the container:
    - `./run_dbg.sh` will start qemu and spawn gdb attached
    - `./run_prod.sh` will start the chall in production environment
