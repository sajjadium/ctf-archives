### README
https://www.iacr.org/archive/crypto2000/18800272/18800272.pdf Claims to be provably secure, what could possible go wrong ^^

We recommend you develop your exploit locally, and have provided you with a docker setup to help :)

To build, use the command `docker build -t blindsign ./` in the folder.
To run, use use the command `docker run -p 4343:4343 --name blindsign blindsign`to run the server, listening on localhost on port 4343. 
You can now communicate with it using nc, or through python using pwntools/telnet. The server receives and sends JSON, which can easily be converted to/from python dictionaries using `json.dumps()` and `json.load()`.

Note that the checkout of the library used is this branch https://github.com/rot256/pblind/tree/serial. (This was just for ease of interacting with the challenge, and shouldn't have any influence on solving compared to master branch.)

Note: The remote server will be restarted periodically. If you are 100% sure you have an efficient reliable solution which works locally, but are having issues with remote due to connection problems, reach out to an admin and we can try and help.