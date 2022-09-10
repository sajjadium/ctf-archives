from application.main import app
from application.database import migrate_db

with app.app_context():
    migrate_db()

app.run(host='0.0.0.0', port=1337, debug=False)