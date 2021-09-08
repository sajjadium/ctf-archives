#!/bin/bash

set -e

echo "This requires sudo access, please enter your password if prompted"

sudo launchctl stop com.alles.sandbox_share
sudo launchctl start com.alles.sandbox_share   
