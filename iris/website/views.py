from flask import Blueprint, render_template, request
from datetime import datetime
from flask_login import current_user
from .models import notice
from . import db

views = Blueprint('views', '__name__')

@views.route('/', methods=['GET', 'POST'])
def portalSelect():
   if request.form:
        notices = notice(title=request.form.get("title"), note=request.form.get("title"))
        db.session.add(notices)
        db.session.commit()
   return render_template("createNotice.html")

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

@views.route('/notices')
def notices():
    return render_template('notices.html')

#@views.route('/createNotices', methods=['GET', 'POST'])
#def createNotices():
#    if request.form:
#        notices = notice(title=request.form.get("title"), note=request.form.get("title"))
#        db.session.add(notices)
#        db.session.commit()
#    return render_template('createNotice.html')