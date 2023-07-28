import sqlite3, os

def query(con, query, args=(), one=False):
    c = con.cursor()
    c.execute(query, args)
    rv = [dict((c.description[idx][0], value)
        for idx, value in enumerate(row) if value != None) for row in c.fetchall()]
    return (rv[0] if rv else None) if one else rv

def db_init():
    con = sqlite3.connect('database/data.db')
    # Create users database
    query(con, '''
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        username text NOT NULL,
        password text NOT NULL
    );
    ''')
            
    query(con, f'''
    INSERT INTO users (
        username,
        password
        ) VALUES (
            'admin',
            '{os.environ.get("ADMIN_PASSWD")}'
        
    );
    ''')
    
    # Create posts database
 
    query(con, ''' 
    CREATE TABLE IF NOT EXISTS posts (
        id integer PRIMARY KEY,
        user_id integer NOT NULL,
        title text,
        content text NOT NULL,
        hidden boolean NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''')


    query(con, f''' 
    INSERT INTO posts (
        user_id,
        title,
        content,
        hidden
        ) VALUES (
            1,
            'Here is a ducky flag!',
            '{os.environ.get("FLAG")}',
            0
        
    );
    ''')

    con.commit()

def db_login(username, password):
    con = sqlite3.connect('database/data.db')
    user = query(con, 'SELECT username FROM users WHERE username = ? AND password = ?', (username, password,), True)
    
    if user:
        return True

    return False

def db_register(username, password):
    con = sqlite3.connect('database/data.db')
    user = query(con, 'SELECT username FROM users WHERE username = ?', (username,), True)

    if not user:
        query(con, 'INSERT into users (username, password) VALUES (?, ?)', (username, password,))
        con.commit()

        return True
    
    return False

def db_create_post(username, post):
    con = sqlite3.connect('database/data.db')

    user = query(con, 'SELECT id from users WHERE username = ?', (username,), True)

    query(con, 'INSERT into posts (user_id, title, content, hidden) VALUES (?, ?, ?, ?)', (user['id'], post['title'], post['content'], post['hidden'],))
    con.commit()

    return True

def db_get_user_posts(username, hidden):
    con = sqlite3.connect('database/data.db')

    posts = query(con, 'SELECT users.username as username, title, content, hidden from posts INNER JOIN users ON users.id = posts.user_id WHERE users.username = ?', (username,))
    return [post for post in posts if hidden or not post['hidden']]

def db_get_all_users_posts():
    con = sqlite3.connect('database/data.db')

    posts = query(con, 'SELECT users.username as username, title, content, hidden from posts INNER JOIN users ON users.id = posts.user_id ')
    return posts

def db_delete_posts(username):
    con = sqlite3.connect('database/data.db')

    user = query(con, 'SELECT id from users WHERE username = ?', (username,), True)

    query(con, 'DELETE FROM posts WHERE user_id = ?', (user['id'], ))
    con.commit()

    return True

def db_delete_all_posts():
    con = sqlite3.connect('database/data.db')

    query(con, 'DELETE FROM posts WHERE id != 1')
    con.commit()

    return True

