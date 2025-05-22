from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_login import current_user
from .models import notice
from . import db

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

@views.route("/editNotice/<int:id>", methods=["GET", "POST"])
def editNotice(id):
    noticeToEdit = notice.query.get(id) #Reading the notice to be edited

    if request.method == "POST":
        #Updating the notice
        noticeToEdit.title = request.form.get("title")
        noticeToEdit.note = request.form.get("note")
        db.session.commit() #Committing the changes to the database
        flash("Notice Updated!", category="success") #Flashing success mesasage
        return redirect(url_for("views.viewNotice")) #Takes user back to the notice page
    
    return render_template("editNotice.html", notices=noticeToEdit) 

@views.route('/deleteNotice', methods=['POST'])
def deleteNotice():
    noitceID = request.form.get("id")
    notices = notice.query.get(noitceID) #Reading the notice to be deleted

    if notices:
        db.session.delete(notices) #Deleting the notice from the database
        db.session.commit() #Committing the changes to the database
    return redirect("/notice")

@views.route('assessmentsLanding')
def assessmentsLanding():
    currentDate = datetime.now().date()
    return render_template("assessmentsLanding.html", user=current_user, currentDate=currentDate)

#@views.route('/notices')
#def notices():
#    return render_template('notices.html')

@views.route('/test-seed')
def test_seed():
    from .models import db, Teacher, Student, Class, TeacherClassAssociation, TeacherRole

    test_class = Class(year=2025, subject='M', code='MATH101')

    teacher = Teacher(
        role='teacher',
        name='Jane Doe',
        email='jane.doe@example.com',
        password='password123',
        gender='F',
        phone_number=123456789,
        address='123 School Lane'
    )

    association = TeacherClassAssociation(
        teacher=teacher,
        class_=test_class,
        role=TeacherRole.MAIN
    )

    student = Student(
        role='student',
        name='John Smith',
        email='john.smith@example.com',
        password='password123',
        gender='M',
        phone_number=987654321,
        address='456 Learning Road'
    )

    student.enrolled_classes.append(test_class)

    db.session.add_all([test_class, teacher, student, association])
    db.session.commit()

    return "Sample data inserted successfully!"