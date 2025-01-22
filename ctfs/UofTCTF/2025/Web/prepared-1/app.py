import re
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import setuptools

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'rootpassword')
DB_NAME = os.getenv('MYSQL_DB', 'prepared_db')

class MaliciousCharacterError(Exception):
    pass

class NonPrintableCharacterError(Exception):
    pass

class DirtyString:
    MALICIOUS_CHARS = ['"', "'", "\\", "/", "*", "+" "%", "-", ";", "#", "(", ")", " ", ","]

    def __init__(self, value, key):
        self.value = value
        self.key = key

    def __repr__(self):
        return self.get_value()

    def check_malicious(self):
        if not all(32 <= ord(c) <= 126 for c in self.value):
            raise NonPrintableCharacterError(f"Non-printable ASCII character found in '{self.key}'.")
        for char in self.value:
            if char in self.MALICIOUS_CHARS:
                raise MaliciousCharacterError(f"Malicious character '{char}' found in '{self.key}'")

    def get_value(self):
        self.check_malicious()
        return self.value

class QueryBuilder:
    def __init__(self, query_template, dirty_strings):
        self.query_template = query_template
        self.dirty_strings = {ds.key: ds for ds in dirty_strings}
        self.placeholders = self.get_all_placeholders(self.query_template)

    def get_all_placeholders(self, query_template=None):
        pattern = re.compile(r'\{(\w+)\}')
        return pattern.findall(query_template)

    def build_query(self):
        query = self.query_template
        self.placeholders = self.get_all_placeholders(query)
        
        while self.placeholders:
            key = self.placeholders[0]
            format_map = dict.fromkeys(self.placeholders, lambda _, k: f"{{{k}}}")
            
            for k in self.placeholders:
                if k in self.dirty_strings:
                    if key == k:
                        format_map[k] = self.dirty_strings[k].get_value()
                else:
                    format_map[k] = DirtyString
                    
            query = query.format_map(type('FormatDict', (), {
                '__getitem__': lambda _, k: format_map[k] if isinstance(format_map[k], str) else format_map[k]("",k)
            })())
            
            self.placeholders = self.get_all_placeholders(query)
            
        return query

def get_db_connection():
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username', '')
        password = data.get('password', '')

        if not username or not password:
            flash("Username and password are required.", 'error')
            return redirect(url_for('login'))

        try:
            du = DirtyString(username, 'username')
            dp = DirtyString(password, 'password')

            qb = QueryBuilder(
                "SELECT * FROM users WHERE username = '{username}' AND password = '{password}'",
                [du, dp]
            )
            sanitized_query = qb.build_query()
            print(f"Sanitized query: {sanitized_query}")
        except (MaliciousCharacterError, NonPrintableCharacterError) as e:
            flash(str(e), 'error')
            return redirect(url_for('login'))
        except Exception:
            flash("Invalid credentials.", 'error')
            return redirect(url_for('login'))

        cnx = get_db_connection()
        if not cnx:
            flash("Database connection failed.", 'error')
            return redirect(url_for('login'))

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(sanitized_query)
            user = cursor.fetchone()
            if user:
                flash("Login successful!", 'success')
                return render_template('under_construction.html')
            else:
                flash("Invalid credentials.", 'error')
        except mysql.connector.Error as err:
            flash(f"Database query failed: {err}", 'error')
        finally:
            cursor.close()
            cnx.close()

    return render_template('login.html')

@app.route('/under_construction')
def under_construction():
    return render_template('under_construction.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
