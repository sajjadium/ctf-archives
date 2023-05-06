#!/bin/bash

service apache2 start;
mkdir /root/tmp/;
(while true;sleep 1200;do rm -rf /tmp/*;done)&
(while true;sleep 1200;do rm -rf /root/tmp/*;done)&
(while true;do sleep 1;php /root/bot.php;done)