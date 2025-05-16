from flask import Blueprint, render_template
from datetime import datetime

views = Blueprint('views', '__name__')

@views.route('/')
def portalSelect():
   currentDate = datetime.now().date()
   return render_template("dashboard.html", currentDate=currentDate)

@views.route('/navBase')
def navBase():
    return render_template("navBase.html")

@views.route('/teacherPortal')
def teacherPortal():
    return render_template('teacherPortal.html')

@views.route('/teacherLogin')
def teacherLogin():
    return render_template('teacherLogin.html')

@views.route('/studentProfile/nameandID')
def studentProfile():
    return render_template('studentProfileName.html')

#@views.route('/dashboard')
#def dashboard():
#   currentDate = datetime.now().date()
#   return render_template('dashboard.html', currentDate=currentDate)