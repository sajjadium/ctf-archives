from app import app, db
from app.models import User, Post

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)