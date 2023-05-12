import json
import os
import secrets
from datetime import timedelta
from decimal import Decimal

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_talisman import Talisman
from flask_talisman.talisman import ONE_YEAR_IN_SECS
from flask_wtf.csrf import CSRFProtect

from flask import Flask, abort

# domain = None  # "127.0.0.1"
domain = "goldinospizza.challs.m0lecon.it"


app = Flask(__name__)


# init extended json encoder
class JSONEncoder(json.JSONEncoder):
    # JSON ENCODER EXTENSION
    def default(self, o):
        if type(o) is Decimal:
            return float(o)
        return json.JSONEncoder.default(self, o)


# init sslify
sslify = SSLify(app)

# init talisman
talisman = Talisman(
    app,
    content_security_policy_nonce_in=["script-src", "style-src"],
    # content_security_policy_nonce_in=["script-src", "style-src"],
    content_security_policy_report_only=False,
    content_security_policy_report_uri=None,
    content_security_policy={  # do not add stuff here, put tags in html template tags: nonce="{{ csp_nonce() }}"
        "default-src": "'none'",
        "script-src": "'self'",
        "style-src": "'self'",
        "img-src": "'self'",
        "connect-src": "'self'",
        "base-uri": "'none'",
        "form-action": "'self'",
        "frame-ancestors": "'none'",
        "strict-dynamic": "",
    },
    feature_policy={},
    force_file_save=True,
    force_https_permanent=True,
    force_https=True,
    frame_options_allow_from=None,
    frame_options="DENY",
    referrer_policy="strict-origin-when-cross-origin",
    session_cookie_http_only=True,
    session_cookie_secure=True,
    strict_transport_security_include_subdomains=True,
    strict_transport_security_max_age=ONE_YEAR_IN_SECS,
    # SOULD BE TRUE, enables HSTS preloading if you register your application with Google's HSTS preload list, Firefox and Chrome will never load your site over a non-secure connection.
    strict_transport_security_preload=False,
    strict_transport_security=True,
)

# init session
app.config.update(
    APPLICATION_ROOT="/",
    JSON_AS_ASCII=True,
    JSON_SORT_KEYS=False,
    JSONIFY_MIMETYPE="application/json",
    JSONIFY_PRETTYPRINT_REGULAR=False,
    MAX_CONTENT_LENGTH=16 * 1000 * 1000,
    MAX_COOKIE_SIZE=4093,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    PREFERRED_URL_SCHEME="https",
    SECRET_KEY=secrets.token_hex(256),
    SEND_FILE_MAX_AGE_DEFAULT=timedelta(hours=12),
    SERVER_NAME=domain,
    SESSION_COOKIE_DOMAIN=domain,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_NAME="session",
    SESSION_COOKIE_PATH="/",
    SESSION_COOKIE_SAMESITE="Strict",
    SESSION_COOKIE_SECURE=True,
    SESSION_REFRESH_EACH_REQUEST=True,
    USE_X_SENDFILE=False,  # disabled: does not work with gunicorn
)

# init flask-wtf
app.config.update(
    # RECAPTCHA_API_SERVER=None,
    # RECAPTCHA_DATA_ATTRS=None,
    # RECAPTCHA_DIV_CLASS="g-recaptcha",
    # RECAPTCHA_HTML=None,
    # RECAPTCHA_PARAMETERS=None,
    # RECAPTCHA_PRIVATE_KEY=None,
    # RECAPTCHA_PUBLIC_KEY=None,
    # RECAPTCHA_SCRIPT="https://www.google.com/recaptcha/api.js",
    # RECAPTCHA_VERIFY_SERVER="https://www.google.com/recaptcha/api/siteverify",
    WTF_CSRF_CHECK_DEFAULT=True,
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_FIELD_NAME="csrf_token",
    WTF_CSRF_HEADERS=["X-CSRFToken", "X-CSRF-Token"],
    WTF_CSRF_METHODS={"POST", "PUT", "PATCH", "DELETE"},
    WTF_CSRF_SECRET_KEY=secrets.token_hex(256),
    WTF_CSRF_SSL_STRICT=True,
    WTF_CSRF_TIME_LIMIT=1200,
    WTF_I18N_ENABLED=True,
)
csrfprotect = CSRFProtect(app)

# init flask-login
app.config.update(
    AUTH_HEADER_NAME="Authorization",
    COOKIE_DURATION=timedelta(minutes=30),
    COOKIE_HTTPONLY=True,
    COOKIE_NAME="remember_token",
    COOKIE_SAMESITE=True,
    COOKIE_SECURE=True,
    EXEMPT_METHODS=set(),
    LOGIN_MESSAGE_CATEGORY="message",
    LOGIN_MESSAGE="Please log in to access this page.",
    REFRESH_MESSAGE_CATEGORY="message",
    REFRESH_MESSAGE="Please reauthenticate to access this page.",
    REMEMBER_COOKIE_DOMAIN=domain,
    REMEMBER_COOKIE_DURATION=timedelta(minutes=30),
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_NAME="remember_token",
    REMEMBER_COOKIE_PATH="/",
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST=True,
    REMEMBER_COOKIE_SECURE=True,
    # SESSION_KEYS=set(["_user_id", "_remember", "_remember_seconds", "_id", "_fresh", "next", ]),
    SESSION_PROTECTION="strong",
    USE_SESSION_FOR_NEXT=True,
)
login_manager = LoginManager(app)

# init flask-sqlalchemy
app.config.update(
    # SQLALCHEMY_DATABASE_URI="sqlite:///:memory:?cache=shared",
    SQLALCHEMY_DATABASE_URI="sqlite:////tmp/db.db",
    # SQLALCHEMY_BINDS={},
    # SQLALCHEMY_ECHO=True,
    # SQLALCHEMY_RECORD_QUERIES=True,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # SQLALCHEMY_ENGINE_OPTIONS={},
)
db = SQLAlchemy(app)


def register_blueprints(app):
    from api import api
    from auth import auth
    from website import website
    app.register_blueprint(auth)
    app.register_blueprint(website)
    app.register_blueprint(api)


register_blueprints(app)

with app.app_context():
    # create all missing db tables
    db.create_all()
    # # default user
    # User.register(
    #     username="user",
    #     password="password",
    # )
    # insert products
    from models import Product, User
    db.session.execute(db.delete(Product))
    db.session.execute(
        db.insert(Product),
        [
            {
                "id": 0,
                "name": "GOLDEN",
                "price": 1e6,
                "description": "The flagship of pizzas",
                "image": "img/GOLDEN.jpg",
                "theme": "golden",
            },
            {
                "id": 1,
                "name": "MARGHERITA",
                "price": 6,
                "description": "Pomodoro, Mozzarella, Basilico",
                "image": "img/MARGHERITA.jpg",
                "theme": "italian",
            },
            {
                "id": 2,
                "name": "MEDITERRANEA",
                "price": 8,
                "description": "Pomodoro, Mozzarella, Tonno, Cipolla",
                "image": "img/MEDITERRANEA.jpg",
                "theme": "italian",
            },
            {
                "id": 3,
                "name": "DIAVOLA",
                "price": 8,
                "description": "Pomodoro, Mozzarella, Salame piccante",
                "image": "img/DIAVOLA.jpg",
                "theme": "italian",
            },
            {
                "id": 4,
                "name": "WÜRSTY",
                "price": 8,
                "description": "Pomodoro, Mozzarella, Würstel",
                "image": "img/WÜRSTY.jpg",
                "theme": "italian",
            },
            {
                "id": 5,
                "name": "VEGGIE",
                "price": 10,
                "description": "Pomodoro, Mozzarella, Zucchine, Melanzane, Peperoni",
                "image": "img/VEGGIE.jpg",
                "theme": "italian",
            },
            {
                "id": 6,
                "name": "COUNTRY",
                "price": 12,
                "description": "Mozzarella, Gorgonzola, Rucola, Funghi, Salsiccia",
                "image": "img/COUNTRY.jpg",
                "theme": "italian",
            },
            {
                "id": 7,
                "name": "BOSCAIOLA",
                "price": 10,
                "description": "Pomodoro, Mozzarella, Prosciutto cotto, Funghi",
                "image": "img/BOSCAIOLA.jpg",
                "theme": "italian",
            },
            {
                "id": 8,
                "name": "4 FORMAGGI",
                "price": 10,
                "description": "Pomodoro, Mozzarella, Scamorza affumicata, Gorgonzola, Grana Padano D.O.P.",
                "image": "img/4_FORMAGGI.jpg",
                "theme": "italian",
            },
            {
                "id": 9,
                "name": "CAPRICCIO",
                "price": 12,
                "description": "Pomodoro, Mozzarella, Prosciutto cotto, Carciofi, Olive , Funghi",
                "image": "img/CAPRICCIO.jpg",
                "theme": "italian",
            },
            {
                "id": 10,
                "name": "VIVALDI",
                "price": 12,
                "description": "Pomodoro, Mozzarella, Prosciutto cotto, Carciofi, Olive, Funghi",
                "image": "img/VIVALDI.jpg",
                "theme": "italian",
            },
            {
                "id": 11,
                "name": "PRIMAVERA",
                "price": 12,
                "description": "Pomodoro, Mozzarella, Rucola, Grana Padano D.O.P., Prosciutto crudo nostrano",
                "image": "img/PRIMAVERA.jpg",
                "theme": "italian",
            },
            {
                "id": 12,
                "name": "BBQ CHICKEN",
                "price": 12,
                "description": "Mozzarella, Cipolla, Salsa BBQ, Pollo",
                "image": "img/BBQ_CHICKEN.jpg",
                "theme": "american",
            },
            {
                "id": 13,
                "name": "BACON & CHICKEN",
                "price": 12,
                "description": "Salsa Greca, Mozzarella, Bacon, Pomodorini, Pollo, Funghi",
                "image": "img/BACON_&_CHICKEN.jpg",
                "theme": "american",
            },
            {
                "id": 14,
                "name": "MEATZZA",
                "price": 15,
                "description": "Salsa Goldino, Mozzarella, Salame piccante, Würstel, Prosciutto cotto, Hamburger, Salsiccia",
                "image": "img/MEATZZA.jpg",
                "theme": "american",
            },
            {
                "id": 15,
                "name": "HAWAIANA",
                "price": 10,
                "description": "Pomodoro, Mozzarella, Prosciutto cotto, Ananas",
                "image": "img/HAWAIANA.jpg",
                "theme": "american",
            },
            {
                "id": 16,
                "name": "CHEESEBURGER",
                "price": 15,
                "description": "Salsa Goldino, Mozzarella, Cheddar, Bacon, Cipolla, Hamburger, Salsa Burger",
                "image": "img/CHEESEBURGER.jpg",
                "theme": "american",
            },
            {
                "id": 17,
                "name": "PEPPERONI PASSION",
                "price": 15,
                "description": "Pomodoro, Mozzarella, Jalapeño rosso, Grana Padano D.O.P., Scamorza affumicata, Doppio Salame piccante, Peperoncino macinato",
                "image": "img/PEPPERONI_PASSION.jpg",
                "theme": "american",
            },
            {
                "id": 18,
                "name": "PACIFIC VEGGIE",
                "price": 12,
                "description": "Salsa Goldino, Mozzarella, Origano, Funghi, Olive, Cipolla, Peperoni, Scamorza affumicata, Rucola (in cottura)",
                "image": "img/PACIFIC_VEGGIE.jpg",
                "theme": "american",
            },
            {
                "id": 19,
                "name": "EXTRAVAGANZZA",
                "price": 15,
                "description": "Pomodoro, Mozzarella, Würstel, Salame piccante, Prosciutto cotto, Cipolla, Funghi, Olive, Peperoni",
                "image": "img/EXTRAVAGANZZA.jpg",
                "theme": "american",
            },
        ]
    )
    db.session.commit()
    # print(db.session.execute(db.select(Product)).scalars().all())


@app.route("/teapot")
async def teapot():
    abort(418)

if __name__ == "__main__":
    app.run()
