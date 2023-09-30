from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Database optimizations
"""@db.event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Uninteresting sqlite optimizations, copied by BeatBuddy
    cursor = dbapi_connection.cursor()
    cursor.execute("pragma journal_mode = WAL")
    cursor.execute("pragma synchronous = normal")
    cursor.execute("pragma temp_store = memory")
    cursor.execute("pragma mmap_size = 30000000000")
    cursor.close()"""