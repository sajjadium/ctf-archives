#!/bin/bash

docker-entrypoint.sh rabbitmq-server &

sleep 20

while [[ true ]]; do
    rabbitmqctl add_user $username $password
    if [[ "$?" != "0" ]]; then
        sleep 5
        continue
    fi

    rabbitmqctl set_permissions $username "^$" "^.*$" "^.*$"
    rabbitmqctl set_user_tags $username management

    rabbitmqadmin declare queue name=email durable=true
    rabbitmqctl delete_user guest

    break
done

echo "Finished setup"

while [[ true ]]; do
    sleep 10000
done