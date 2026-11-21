#!/usr/bin/env bash

# prompt users when removing whole directories
# used when making target "mrproper"

read -p "$1" answer_from_user

# early exit for lazy users
if [[ -z $answer_from_user ]]; then
  exit 0
fi

# proper case handling
case $answer_from_user in
	[Yy]* ) exit 0;;
	* ) exit -1;;
esac
