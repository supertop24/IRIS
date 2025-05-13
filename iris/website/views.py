from flask import Blueprint, render_template

views = Blueprint('views', '__name__')

@views.route('/')
def portalSelect():

   return render_template("portalSelect.html")

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