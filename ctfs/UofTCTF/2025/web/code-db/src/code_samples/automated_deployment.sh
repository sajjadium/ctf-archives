#!/bin/bash

# Variables
APP_DIR="/var/www/myapp"
REPO_URL="https://github.com/user/myapp.git"
BRANCH="main"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y git nginx

# Clone repository
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
    git pull origin $BRANCH
else
    git clone -b $BRANCH $REPO_URL $APP_DIR
    cd "$APP_DIR"
fi

# Install application dependencies
# Assuming it's a Node.js app
sudo apt install -y nodejs npm
npm install

# Restart services
sudo systemctl restart nginx
sudo systemctl restart myapp
echo "Deployment completed successfully."
