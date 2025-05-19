from flask import Blueprint, render_template
from datetime import datetime
from flask_login import current_user

views = Blueprint('views', '__name__')

@views.route('/')
def portalSelect():
   return render_template("topbanner.html")

@views.route('/navBase')
def navBase():
    return render_template("navBase.html")

@views.route('/teacherPortal')
def teacherPortal():
    return render_template('teacherPortal.html', user=current_user)

@views.route('/studentProfile/nameandID')
def studentProfile():
    return render_template('studentProfileName.html')

@views.route('/dashboard')
def dashboard():
   currentDate = datetime.now().date()
   return render_template('dashboard.html', currentDate=currentDate)

#@views.route('/notices')
#def notices():
#    return render_template('notices.html')