#! /bin/bash
service nginx start
sleep 3

export PORT='80'
export ADMIN_BOT_USER="admin"
export ADMIN_BOT_PASSWORD="<REDACTED>"

export CHALLENGE_NAME="AgentTester" && export CHALLENGE_FLAG="<REDACTED>"\
    && uwsgi --ini app.ini