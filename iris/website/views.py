from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_login import current_user
from .models import notice
from . import db

views = Blueprint('views', '__name__')

@views.route('/')
def portalSelect():
   return render_template('portalSelect.html')

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

@views.route('/notice')
def viewNotice():
    allNotices = notice.query.all() #Reading all the notices
    return render_template('notice.html', allNotices=allNotices)

@views.route('/createNotice', methods=['GET', 'POST'])
def createNotice():
   if request.method == 'POST':
       #Creating new notice
       newNotice = notice( 
        title=request.form.get("title"),
        note=request.form.get("note")
        )
       db.session.add(newNotice) #Adding new notice to the database
       db.session.commit() #Committing new notice to the database

       #Flash message to show that the notice has been created
       flash("Notice Created!", category="success")
       return redirect(url_for('views.viewNotice')) #Takes user back to the notice page
   return render_template("createNotice.html")

@views.route("/updateNotice", methods=["POST"])
def update():
    newTitle = request.form.get("newTitle")
    oldTitle = request.form.get("oldTitle")
    notices = notice.query.filter_by(title=oldTitle).first() #Reading the notice to be updated
    notices.notice = newTitle #Updating the notice's title
    db.session.commit() #Committing the changes to the database
    return redirect(url_for('views.viewNotice')) #Takes user back to the notice page