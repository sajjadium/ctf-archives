from flask import Blueprint, flash, render_template
from flask_login import current_user, login_required

from .. import db
from ..form import WebhookForm
from ..model import Space

main = Blueprint("main", __name__)


@main.route("/")
def home():
    spaces = Space.query.all()
    return render_template("home.html", spaces=spaces)


@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = WebhookForm()
    if form.validate_on_submit():
        current_user.webhook = form.webhook.data
        db.session.add(current_user)
        db.session.commit()
        flash("webhook updated")
    return render_template("profile.html", form=form)
