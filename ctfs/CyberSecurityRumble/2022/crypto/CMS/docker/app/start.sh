PYTHONDONTWRITEBYTECODE=1 python -c 'import main' # prepare database and stuff
gunicorn --workers 4 --threads 4 --bind 0.0.0.0:8000 --chdir /app main:app
