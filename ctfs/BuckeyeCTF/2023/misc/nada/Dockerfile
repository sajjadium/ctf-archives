FROM nixos/nix

RUN nix-channel --update
RUN nix-env -iA nixpkgs.nix-serve nixpkgs.python3Packages.supervisor nixpkgs.bun

WORKDIR /app

RUN mkdir submissions

COPY package.json package.json
COPY bun.lockb bun.lockb

RUN bun install

COPY flag.txt flag.txt
COPY app.ts app.ts

COPY supervisord.conf /etc/supervisord.conf
CMD supervisord
