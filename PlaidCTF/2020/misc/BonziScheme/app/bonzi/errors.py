from flask import render_template, redirect, url_for
from bonzi import app
from bonzi.acsparse import ACSParseException
from bonzi.forms import ACSSubmitForm
from werkzeug.exceptions import RequestEntityTooLarge

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", message="No buddies here :(")

@app.errorhandler(ACSParseException)
def acs_parse_exception(error):
    form = ACSSubmitForm()
    return render_template("buddy.html", form=form, error_message={"ACSParseException": [error]})
