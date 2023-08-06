#!/bin/bash
docker build --tag=pinder .
docker run -p 80:80  --rm --name=pinder -it pinder