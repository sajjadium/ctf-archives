from flask import request, jsonify, Blueprint, current_app, make_response, render_template, redirect, url_for
from src.auth import requires_token, is_authenticated, token_value, requires_teacher, is_teacher_role
import random

api = Blueprint('api', __name__)

def ran_g():
    grades = ['A', 'B', 'C', 'D', 'E', 'F']
    return random.choice(grades)

@api.route('/')
def index():
    if is_teacher_role():
        return render_template('public.html', is_auth=True, is_teacher_role=True)
    elif is_authenticated():
        return render_template('public.html', is_auth=True)
    return render_template('public.html')

@api.route('/signup', methods=('POST', 'GET'))
def signup():

    # make sure user isn't authenticated
    if is_teacher_role():
        return render_template('public.html', is_auth=True, is_teacher_role=True)
    elif is_authenticated():
        return render_template('public.html', is_auth=True)

    # get form data
    if request.method == 'POST':
        jwt_data = request.form.to_dict()
        jwt_cookie = current_app.auth.create_token(jwt_data)
        if is_teacher_role():
            response = make_response(redirect(url_for('api.index', is_auth=True, is_teacher_role=True)))
        else:
            response = make_response(redirect(url_for('api.index', is_auth=True)))
        
        response.set_cookie('auth_token', jwt_cookie, httponly=True)
        return response

    return render_template('signup.html')

@api.route('/grades')
@requires_token
def grades():
    token = request.cookies.get('auth_token')
    number, email, role_bool = token_value(token)
    role = "Student" if not role_bool else "Teacher"
    if is_teacher_role():
        return render_template('grades.html', is_auth=True, number=number, email=email, role=role, mg=ran_g(), eg=ran_g(), sg=ran_g(), gg=ran_g(), ag=ran_g(), is_teacher_role=True)
    return render_template('grades.html', is_auth=True, number=number, email=email, role=role, mg=ran_g(), eg=ran_g(), sg=ran_g(), gg=ran_g(), ag=ran_g())

@api.route('/grades_flag', methods=('GET',))
@requires_teacher
def flag():
    return render_template('flag.html', flag="FAKE{real_flag_is_on_the_server}", is_auth=True, is_teacher_role=True)

@api.route('/logout')
def logout():
    response = make_response(redirect(url_for('api.index')))
    response.delete_cookie('auth_token')
    return response
