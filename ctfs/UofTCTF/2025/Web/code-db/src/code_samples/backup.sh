#!/bin/bash

SOURCE_DIR="$HOME/Documents"
BACKUP_DIR="$HOME/Backup"

mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.tar.gz"

tar -czf "$BACKUP_FILE" "$SOURCE_DIR"

echo "Backup of $SOURCE_DIR completed at $BACKUP_FILE"
