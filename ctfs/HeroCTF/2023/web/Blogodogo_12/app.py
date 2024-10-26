#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, flash
import lorem
from sqlalchemy.exc import IntegrityError

import os
import random
from secrets import token_hex
from datetime import datetime

from config import TestConfig, db, login_manager
from src.routes import bp_routes
from src.models import Authors, Posts
from src.utils import generate_hash


def create_app():
    app = Flask(__name__)

    app.config.from_object(TestConfig)

    login_manager.init_app(app)
    db.init_app(app)
    app.register_blueprint(bp_routes)

    with app.app_context():
        db.create_all()

        @login_manager.user_loader
        def load_user(author_id):
            return Authors.query.get(int(author_id))

        @login_manager.unauthorized_handler
        def unauthorized_callback():
            flash("You need to be authenticated.", "warning")
            return redirect(url_for('bp_routes.login'))


        # ... SKIPPED

        db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
