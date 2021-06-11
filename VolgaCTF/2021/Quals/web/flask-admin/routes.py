from app import app, db
from flask import render_template, render_template_string, request, flash, redirect, url_for, send_from_directory, make_response, abort
import flask_admin as admin
from flask_admin import Admin, expose, base
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from app.models import User, Role
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators, widgets,fields, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.decorators import admin_required, user_required
from werkzeug.urls import url_parse
import os

#-------------------------Admins-------------------------
class MyAdmin(admin.AdminIndexView):
    @expose('/')
    @admin_required
    def index(self):
        return super(MyAdmin, self).index()

    @expose('/user')
    @expose('/user/')
    @admin_required
    def user(self):
        return render_template_string('TODO, need create custom view')

admin = Admin(app, name='VolgaCTF', template_mode='bootstrap3', index_view=MyAdmin())
admin.add_view(ModelView(User, db.session))
#--------------------------------------------------------


#-------------------------Forms-------------------------
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "username"})
    email = StringField('Email', validators=[DataRequired(), validators.Length(1, 64), Email()],render_kw={"placeholder": "admin@admin.ru"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "password"})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "password"})
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
#-------------------------------------------------------


@app.route('/')
def index():
    if current_user and current_user.is_authenticated and current_user.role.name == 'Administrator':
        return os.environ.get('Volga_flag') or 'Error, not found flag'
    return 'Hello, to get the flag, log in as admin'



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            # Keep the user info in the session using Flask-Login
            login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


def permission_check(permission):
    flag = False
    try:
        if current_user.can(permission):
            return True
        else:
            return False
    except AttributeError:
        return False
    return flag

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
