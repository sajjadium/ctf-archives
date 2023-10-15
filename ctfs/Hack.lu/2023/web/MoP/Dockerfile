# The container will run without internet access!
# docker build -t challenge . && docker run --rm --cap-drop=ALL --cap-add=NET_BIND_SERVICE -p80:80 challenge
FROM nixos/nix:2.16.0 as deps

WORKDIR /challenge

COPY flake.lock flake.nix readflag.c ./

RUN nix --extra-experimental-features "nix-command flakes" build .#readFlag

RUN mv result/bin/readflag /readflag && chown 0:0 /readflag && chmod u+s /readflag

COPY app ./app

RUN nix --extra-experimental-features "nix-command flakes" build .#

COPY flag /flag
RUN chown 0:0 /flag && chmod 400 /flag

USER nobody
CMD result/bin/challenge-server
