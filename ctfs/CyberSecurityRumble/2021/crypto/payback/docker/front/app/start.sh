dd if=/dev/urandom of=/secret bs=1 count=32
PYTHONDONTWRITEBYTECODE=1 python -c 'import app' # prepare database and stuff
gunicorn --preload --workers 4 --threads 4 --bind 0.0.0.0:5000 --chdir /app app:app