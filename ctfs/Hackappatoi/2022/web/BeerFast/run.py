import app
from app.bot import run_bot

if __name__ == "__main__":
    application, admin_usr, admin_pwd = app.create_app(__name__, config=None)
    run_bot(admin_usr, admin_pwd)
    application.run(host="0.0.0.0", port=8000, debug=False)
