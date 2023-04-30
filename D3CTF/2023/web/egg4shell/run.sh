#!/usr/bin/env bash
cd /app
useradd -m app
chown -R app:root /app
su app -c '`npm bin`/egg-scripts start --title=egg-server-egg4shell'
