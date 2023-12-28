#!/bin/bash

cleanup ()
{
kill -s SIGKILL $!
exit 0
}

trap cleanup SIGINT SIGTERM

until false
do
  ./wait_for_can.sh
  ./heater
  sleep 2
done

exit
