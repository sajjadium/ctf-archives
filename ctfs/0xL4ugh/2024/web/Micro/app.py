from flask import Flask, request
import mysql.connector, hashlib

app = Flask(__name__)

# MySQL connection configuration
mysql_host = "127.0.0.1"
mysql_user = "ctf"
mysql_password = "ctf123"
mysql_db = "CTF"

def authenticate_user(username, password):
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )

        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result  
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

@app.route('/login', methods=['POST'])
def handle_request():
    try:
        username = request.form.get('username')
        password = hashlib.md5(request.form.get('password').encode()).hexdigest()
        # Authenticate user
        user_data = authenticate_user(username, password)

        if user_data:
            return "0xL4ugh{Test_Flag}"  
        else:
            return "Invalid credentials"  
    except:
        return "internal error happened"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
