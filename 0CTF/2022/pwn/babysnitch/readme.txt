Summary for `service.py`: we'll throw whatever you provided into a new container and run it, hope you can get flag here.

I don't want to add a hard PoW. Please do not bruteforce and test on your local deployment first.

To build a local environment:
1. Enter `docker` dir, and download opensnitch_1.5.2-1_amd64.deb from opensnitch_1.5.2-1_amd64.deb.url first.
2. Running `docker build -t chal .`.
3. Running `service.py` with things like socat on your host machine.
