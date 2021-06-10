#!/bin/bash

opam repo set-url -y default git+https://github.com/ocaml/opam-repository.git
opam repo add -y janestreet-124.17 git+https://github.com/janestreet/opam-repository.git#016331f5090a45e54e7840836b4720424c58c405
opam repo add -y janestreet-external-124.17 git+https://github.com/janestreet/opam-repository.git#aa1897b74a2e07bf63cc60ae1286dbd05f1848a1
