#! /bin/bash

if ! [[ "$(npm list -g huffc)" =~ "empty" ]]; then
  # huffc was installed via npm, return 0x00
  echo -n 0x00
elif [[ "$(yarn global list)" =~ "huffc" ]]; then
  # huffc was installed via yarn, return 0x00
  echo -n 0x00
else
  echo -n 0x01
fi
