#!/bin/bash

docker build -t three_oracles .
docker run -p 3000:3000 --rm --name three_oracles -t three_oracles
