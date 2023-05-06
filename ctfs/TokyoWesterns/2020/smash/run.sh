#!/bin/sh

cd `dirname $0`
echo "Now loading..."
env -i ./sde/sde64 -no-follow-child -cet -cet_output_file /dev/null -- ./smash
