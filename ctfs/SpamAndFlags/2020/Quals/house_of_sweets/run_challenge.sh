#!/bin/bash
set -euo pipefail

echo "Starting. It takes around 20 seconds..."
./emulator -avd cicaavd -no-audio -no-window -selinux permissive >/dev/null 2>/dev/null&
sleep 5
adb root >/dev/null 2>/dev/null
adb shell /data/local/tmp/house_of_sweets
