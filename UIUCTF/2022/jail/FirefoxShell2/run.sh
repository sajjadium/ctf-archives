#!/bin/sh

/usr/bin/xvfb-run /usr/bin/firefox \
  -app /home/user/app/application.ini \
  --purgecaches --no-remote \
  --introname "Firefox CLI 2: The Sandbox" --hardened
