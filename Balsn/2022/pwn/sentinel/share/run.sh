#!/bin/bash

exec timeout 1800 python3 /home/sentinel/instanceManager.py /tmp2/instances/ /home/sentinel/guest_home/ 24 dummySecret
