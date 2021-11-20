#!/bin/bash

for f in /home/${USERNAME}/startup/*; do
    echo "[+] running $f"
    bash "$f"
done

tail -f /var/log/${USERNAME}/*
