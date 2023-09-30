#!/bin/bash
if [ "$( docker container inspect -f '{{.State.Running}}' $1 )" = "true" ]; then
    exit 0
else
    exit 1
fi