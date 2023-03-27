#!/bin/bash
set -e

mkdir -p log 2>/dev/null
chmod o+w log

docker compose build
