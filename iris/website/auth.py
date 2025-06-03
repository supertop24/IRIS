from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Teacher
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from website.sqlite_helper import get_db

auth = Blueprint('auth', '__name__')
                 
@auth.route('/teacherLogin', methods=['GET', 'POST']) 
def teacherLogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                flash('Logged in successfully!', category='success')
                login_user(user)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect pw', category='error')
        else: 
            flash ('Email not exist', category='error')


    return render_template("teacherLogin.html", user=current_user)

