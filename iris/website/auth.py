from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from website import db

auth = Blueprint('auth', '__name__')
                 
@auth.route('/teacherLogin', methods=['GET', 'POST']) 
def teacherLogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        User = user.query.filter_by(email=email).first()
        if User:
            if password == User.password:
                flash('Logged in successfully!', category='success')
                login_user(User)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect pw', category='error')
        else: 
            flash ('Email not exist', category='error')


    return render_template("teacherLogin.html", User=current_user)

