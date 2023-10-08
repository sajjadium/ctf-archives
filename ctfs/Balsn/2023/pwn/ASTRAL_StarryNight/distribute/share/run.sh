#!/bin/bash

exec 2>/dev/null

cd /home/Astral
timeout 150 /home/Astral/hypervisor /home/Astral/processor /home/Astral/kernel /home/Astral/user 150
