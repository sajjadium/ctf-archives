#!/bin/sh

echo "pruning old chromium processes"

ps -eao command,pid -o etime | ps -eao command,pid -o etimes | grep chromium | awk '{if ($3 > 600) print $2}' | xargs kill -9

echo "Killed all chromium processes older than 600 seconds"