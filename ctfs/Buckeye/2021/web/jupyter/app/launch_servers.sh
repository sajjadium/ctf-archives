#!/usr/bin/env sh
python -m jupyter notebook \
    --notebook-dir=$UPLOADS_DIR \
    --NotebookApp.token=$JUPYTER_TOKEN \
    --NotebookApp.ip='*' \
    --no-browser &
mkdir -p /tmp/uploads
python server.py
