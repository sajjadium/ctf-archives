from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import cache, db
from ..form import PostForm, SpaceForm
from ..model import Post, Space, Subscription
from ..notify import notify

space = Blueprint("space", __name__)


def get_subscription(user, space):
    query = Subscription.query.filter_by(user=user).filter_by(space=space)
    return query.first()


@cache.memoize(timeout=60)
def num_subscriptions(space_id):
    return len(Subscription.query.filter_by(space_id=space_id).all())


@space.route("/space/<space_id>")
def view(space_id):
    space = Space.query.get(space_id)
    if space is None:
        return abort(404)
    subscribed = None
    if current_user.is_authenticated:
        subscribed = get_subscription(current_user, space) is not None
    subs = num_subscriptions(space.id)
    return render_template("space.html", subscribed=subscribed, subs=subs, space=space)


@space.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = SpaceForm()
    if form.validate_on_submit():
        space = Space(name=form.name.data, user=current_user)
        db.session.add(space)
        db.session.commit()
        flash("space created")
        return redirect(url_for("space.view", space_id=space.id))
    return render_template("create.html", form=form)


@space.route("/space/<space_id>/post", methods=["GET", "POST"])
@login_required
def post(space_id):
    space = Space.query.get(space_id)
    if space is None:
        return abort(404)
    if space.user_id != current_user.id:
        return abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, space=space)
        db.session.add(post)
        db.session.commit()
        notify(post)
        flash("post created")
        return redirect(url_for("space.view", space_id=space.id))
    return render_template("post.html", form=form, space=space)


@space.route("/space/<space_id>/sub")
@login_required
def sub(space_id):
    space = Space.query.get(space_id)
    if space is None:
        return abort(404)
    if get_subscription(current_user, space) is None:
        subscription = Subscription(user=current_user, space=space)
        db.session.add(subscription)
        db.session.commit()
        flash("subscribed")
    return redirect(url_for("space.view", space_id=space.id))


@space.route("/space/<space_id>/unsub")
@login_required
def unsub(space_id):
    space = Space.query.get(space_id)
    if space is None:
        return abort(404)
    subscription = get_subscription(current_user, space)
    if subscription is not None:
        db.session.delete(subscription)
        db.session.commit()
        flash("unsubscribed")
    return redirect(url_for("space.view", space_id=space.id))
