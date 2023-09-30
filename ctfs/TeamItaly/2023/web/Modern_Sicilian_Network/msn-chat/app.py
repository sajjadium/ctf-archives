import os
import uuid
from datetime import datetime
from flask import Flask
from utils.models import *

SECRET_KEY = os.getenv("SECRET_KEY")
DOMAIN = os.getenv("DOMAIN")
CHAT_PORT = os.getenv("CHAT_PORT")
SPACES_PORT = os.getenv("SPACES_PORT")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_DOMAIN"] = f".{DOMAIN}"

from utils.db import db
db.init_app(app)
with app.app_context():
    db.create_all()
    ### FOLLOWING CODE CREATES DEFAULT USERS, MESSAGES AND ARTICLES FOR THE CHALLENGE
    if not User.query.filter_by(username="Tofu").first():
        
        catId = str(uuid.uuid4())
        cat = User(catId, "Tofu", str(uuid.uuid4()), "tofu.png")
        db.session.add(cat)
        
        adminId = str(uuid.uuid4())
        admin = User(adminId, "Loldemort", ADMIN_PASSWORD, "arancina.jpg")
        db.session.add(admin)

        db.session.commit()
        
        meow = Message(str(uuid.uuid4()), 0, "Meow!", datetime.utcnow(), admin, cat)
        flag = Message(str(uuid.uuid4()), 0, os.getenv("FLAG", "flag{test}"), datetime.utcnow(), cat, admin)
        db.session.add(meow)
        db.session.add(flag)
        
        db.session.commit()
        
        catArticleId = str(uuid.uuid4())
        title = "Meow!"
        content = f"Purr meow!!<br /><br /><img src='//chat.{DOMAIN}:{CHAT_PORT}/static/propic/tofu-knows-what-you-are.jpg' width='300' /><br /><b>I know what you are.</b>"
        catArticle = Article(catArticleId, catId, datetime.utcnow(), title, content)
        db.session.add(catArticle)
        
        adminArticleId = str(uuid.uuid4())
        title = "Hi, my new friend!"
        content = \
f'''Hi! Nice to see you here! Are you from Sicily? If so, are you from the nice or the evil side of the island?
<br /><br />
If you don't know what it means, it all comes down to the <a href="https://www.streaty.com/blog/arancini-or-arancina/">arancina-vs-arancino</a> civil war.
<br />
Being a matter of the utmost importance and seriousness, you should know that I joined the war on the side of the arancina.
<br /><br />
But setting politics aside, let's talk and become friends!
<br />
I love reading and have nothing to read these days. Do you have any interesting articles to recommend?
<br />
I'm constantly arguing with cat Tofu, so I may not answer quickly... please send a nudge if you message me.'''
        adminArticle = Article(adminArticleId, adminId, datetime.utcnow(), title, content)
        db.session.add(adminArticle)
        
        title = "Welcome to MSN!"
        content = \
f'''Our team is extremely happy to welcome you on this exciting new platform!
<br />
Some articles that may be worth reading:
<ul>
    <li><a href="/articles/{catId}/{catArticleId}">Tofu's article</a>, to know more about our values</li>
    <li>My personal <a href="/articles/{adminId}/{adminArticleId}">welcome letter</a> to all new members</li>
</ul>
<b>NEW!</b> We created a revolutionary feature to catch busy users' attention, the Nudge!
<br />
Press the <img src="//chat.{DOMAIN}:{CHAT_PORT}/static/style/assets/chat-window/414.png" alt="Nudge" /> button in chat to try it.
<br />
Note that to prevent abuse, your browser will calculate proof of works in background each time you send a nudge. The calculation will take some seconds.'''
        
        welcomeArticle = Article(str(uuid.uuid4()), adminId, datetime.utcnow(), title, content)
        db.session.add(welcomeArticle)
        db.session.commit()


@app.after_request
def csp(r):
    r.headers["Content-Security-Policy"] = f"default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-eval'; img-src 'self' data:; connect-src 'self' spaces.{DOMAIN}:{SPACES_PORT}"
    return r

from utils.socket import socket
socket.init_app(app)

from routes import api
app.register_blueprint(api.bp)

from routes import client
app.register_blueprint(client.bp)