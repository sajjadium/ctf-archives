#!/bin/bash

set -e

/bin/echo -n "Enter the path to your exploit: "
read EXPLOIT_PATH

EXPLOIT_PATH=$(realpath $EXPLOIT_PATH)

cp $EXPLOIT_PATH /private/tmp/sandbox_share_exploit
EXPLOIT_PATH=/private/tmp/sandbox_share_exploit

echo "Ensuring exploit is readable for user nobody"
chmod o+rx "$EXPLOIT_PATH"

echo "Creating sandbox profiles..."
cat /usr/local/share/sandbox_share_exploit.sb | python3 -c '__import__("sys").stdout.write(__import__("sys").stdin.read().replace("PROGRAM_NAME", __import__("sys").argv[1]).replace("PROGRAM_DIR", __import__("os").path.dirname(__import__("sys").argv[1])))' "$EXPLOIT_PATH" | tee /tmp/exploit.sb >/dev/null

set +e

launchctl print system/com.alles.sandbox_share >/dev/null
RES=$?

set -e

if [ $RES -ne 0 ]; then
	echo "Service not running, starting now"
	echo "This requires sudo access, please enter your password if prompted"
	sudo launchctl load /Library/LaunchDaemons/com.alles.sandbox_share.plist
fi

echo "Starting client"

trap 'kill $(jobs -p)' SIGINT SIGTERM EXIT

sandbox-exec -f /usr/local/share/sandbox_share_client.sb /usr/local/bin/sandbox_share_client com.alles.sandbox_share &

echo "Starting exploit"

sandbox-exec -f /tmp/exploit.sb "$EXPLOIT_PATH" com.alles.sandbox_share
