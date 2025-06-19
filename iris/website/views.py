from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, request, abort
from datetime import datetime, date, timedelta, time
from flask_login import current_user, login_required
from .models import notice, Class, Student, Teacher, ClassSession, Period, TeacherClassAssociation, TeacherRole, User, Pastoral, Award, Flags
from . import db
from collections import defaultdict
import re

views = Blueprint('views', '__name__')

#Declaring for awards page
awardsByYear = defaultdict(list)

def getMyClasses():

    userId = current_user.id

    myClassFinder = TeacherClassAssociation.query.filter(
        TeacherClassAssociation.teacher_id == userId
    ).all()

    myClassesIds = [assoc.class_id for assoc in myClassFinder]
    
    myClasses = Class.query.filter(
        Class.id.in_(myClassesIds)
    ).all()

    return myClasses

def getOtherClasses():

    userId = current_user.id 

    associations = TeacherClassAssociation.query.filter(
        TeacherClassAssociation.teacher_id != userId
    ).all()

    otherClasses = [
        (assoc.class_, assoc.teacher.name) for assoc in associations
    ]

    return otherClasses
    


def getCOFromTCA():
    classObject = TeacherClassAssociation.query.all()
    return classObject

@views.route('/')
def student():
   #Getting all awards
   allAwards = Award.query.all()
   
   return render_template("portalselect.html")

@views.route('/navBase')
def navBase():
    return render_template("navBase.html")

@views.route('/portalSelect')
def portalSelect():
    return render_template('portalSelect.html')

@views.route('/teacherPortal')
def teacherPortal():
    return render_template('teacherPortal.html', user=current_user)

@views.route('/studentProfile/<int:student_id>')
def studentProfile(student_id):

    allFlags = Flags.query.filter_by(student_id=student_id).all() # Getting all flags associated with user

    allPastoralReports = Pastoral.query.all() #Getting all pastoral reports - no filtering yet
    
    #Getting awards for the specific student
    allAwards = Award.query.filter_by(student_id=student_id).all()

    #Grouping awards by year
    awardsByYear = defaultdict(list)
    for award in allAwards:
        awardsByYear[award.year].append(award)

    #Converting to regular dict and sorting by year from newest to oldest
    awardsByYear = dict(sorted(awardsByYear.items(), key=lambda x: x[0], reverse=True))

    return render_template('student.html', student_id=student_id, allPastoralReports=allPastoralReports, pastoral=None, allAwards=allAwards, awardsByYear=awardsByYear)

@views.route('/searchStudent')
def searchstudent():
    return render_template('showstudent.html')

@views.route('/communication')
def communicationC():
    return render_template('communicationcenter.html')

@views.route('/dashboard')
def dashboard():
   currentDate = datetime.now().date()
   return render_template('dashboard.html', user=current_user, currentDate=currentDate)

# Adding API endpoint for getting teacher schedule data here with dashboard route - this is where it'll be used
@views.route('/api/daily-schedule')
@login_required
def api_daily_schedule():
    print("Logged in user:", current_user.id, current_user.__class__.__name__) # Console check for the logged in user 

    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
    
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    print("API request date:", selected_date) # Console check for date requested

    if isinstance(current_user, (Student, Teacher)):
        try:
            schedule = current_user.get_daily_schedule(selected_date)
            print(f"Found {len(schedule)} sessions for {current_user.__class__.__name__}") # Another console check, so we can make this function work !!!
        except Exception as e:
            print(f"Error getting schedule: {e}")
            return jsonify({'error': 'Failed to retrieve schedule'}), 500
    else:
        print("User is not a Teacher or Student.")
        return jsonify([])

    serialized = []
    for session in schedule:
        try:
            session_data = {
                'class_code': session.class_.code if session.class_ else None,
                'subject': session.class_.subject if session.class_ else None,
                'period_id': session.period.id if session.period else None,
                'period_label': session.period.label if (session.period and hasattr(session.period, 'label')) else f"P{session.period.id}" if session.period else None,
                'period_code': session.period.code if session.period else None,
                'start_time': session.period.start_time.strftime('%H:%M') if session.period and session.period.start_time else None,
                'end_time': session.period.end_time.strftime('%H:%M') if session.period and session.period.end_time else None,
                'date': session.date.isoformat()
            }
            serialized.append(session_data)
        except Exception as e:
            print(f"Error serializing session {session.id}: {e}")
            continue

    print("Serialized sessions:", serialized)
    return jsonify(serialized)

@views.route('/attendanceLanding')
def attendanceLanding():
    currentDate = datetime.now().date()
    myClasses = getMyClasses()
    otherClasses = getOtherClasses()
    return render_template("assessmentsLanding.html", user=current_user, currentDate=currentDate, myClasses = myClasses, otherClasses = otherClasses)

@views.route('/studentsLanding')
def studentsLanding():
    currentDate = datetime.now().date()
    myClasses = getMyClasses()
    otherClasses = getOtherClasses()
    return render_template("studentsLanding.html", user=current_user, currentDate=currentDate, myClasses = myClasses, otherClasses = otherClasses)

@views.route('/pastoralLanding')
def pastoralLanding():
    currentDate = datetime.now().date()
    myClasses = getMyClasses()
    otherClasses = getOtherClasses()
    return render_template("pastoralLanding.html", user=current_user, currentDate=currentDate, myClasses = myClasses, otherClasses = otherClasses)

@views.route('/reportsLanding')
def reportsLanding():
    currentDate = datetime.now().date()
    myClasses = getMyClasses()
    otherClasses = getOtherClasses()
    return render_template("reportsLanding.html", user=current_user, currentDate=currentDate, myClasses = myClasses, otherClasses = otherClasses)

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

@views.route('/pastoralReports')
def viewPastoralReports():
    allPastoralReports = Pastoral.query.all() #Reading all the pastoral reports for the student
    return render_template('awards.html', allPastoralReports=allPastoralReports)

@views.route('/pastoralReport/<int:id>')
def pastoralReport(id):
    pastoral = Pastoral.query.get_or_404(id) #Getting the report's id and passing it to the template
    return render_template('student.html', pastoral=pastoral)

@views.route('createPastoralIncidentReport', methods=['POST'])
def createPastoralIncidentReport():
    if request.method == 'POST':
        newReport = Pastoral(
            date=request.form.get("date"),
            time=request.form.get("time"),
            location=request.form.get("location"),
            type=request.form.get("type"),
            studentsInvolved=request.form.get("studentsInvolved"),
            staffInvolved=request.form.get("staffInvolved"),
            author=request.form.get("author")
        )
        db.session.add(newReport) #Adding new notice to the database and committing it
        db.session.commit()
        flash("Pastoral Report Created!", category="success")
        return redirect(url_for('views.viewPastoralReports'))
    
@views.route('individualPastoralReport')
def individualPastoralReport():
    print("testing if the individual page is showing")
    return render_template('pastoral.html')

@views.route('/uploadAward', methods=['POST'])
def uploadAward():
    try:
        #Getting JSON data from the request
        data = request.get_json()

        #Validating required fields
        if not data.get('term') or not data.get('grade'):
            return jsonify({'success': False, 'message': 'Term and Grade are required'})
        
        #Converting term and grade from the dropdown values to their actual values
        termMapping = {
            '1': 'First Term',
            '2': 'Second Term',
            '3': 'Third Term',
            '4': 'Fourth Term'
        }

        gradeMapping = {
            '1': 'Year 9',
            '2': 'Year 10',
            '3': 'Year 11',
            '4': 'Year 12',
            '5': 'Year 13'
        }

        #Creating a new award object
        newAward = Award(
            term=termMapping.get(data['term'], data['term']),
            type=data.get('type', ''),
            note=data.get('title', ''),
            grade=gradeMapping.get(data['grade'], data['grade']),
            subject=data.get('subject', ''),
            year=data.get('year'),
            student_id=data.get('student_id') #passing the student id
        )

        #Adding it to the data.base
        db.session.add(newAward)
        db.session.commit()

        return jsonify({'success': True, 'message':'Award uploaded successfully!'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@views.route('assessmentsLanding')
def assessmentsLanding():
    currentDate = datetime.now().date()
    myClasses = getMyClasses()
    otherClasses = getOtherClasses()
    return render_template("assessmentsLanding.html", user=current_user, currentDate=currentDate, myClasses = myClasses, otherClasses = otherClasses)



@views.route('/morePopulating')
def morePopulating():
    try:
        teacher = Teacher(
            name = "Jane Smith",
            email = "janesmith@school.com",
            password="janesmith",
            gender = "Female",
            phone_number = "09 123 456",
            address = "12 NoOnion Street"
        )
        db.session.add(teacher)
        db.session.flush()

        period = Period.query.order_by(Period.id).limit(5).all()
        if len(period) < 5:
            raise Exception("Not enough periods in the database to assign sessions.")

        subjects = ["Year 10 Mathematics", "Year 10 Science", "Year 11 Biology", "Year 11 Chemistry", "Year 11 Physics"]
        classes=[]
        for i, subject in enumerate(subjects):

            parts = subject.split()
            year = parts[1]
            abr = parts[2][:3].upper()
            clsCode = f"{year}{abr}1"
            cls = Class(year=2025, subject=subject, code=clsCode)
            db.session.add(cls)
            db.session.flush()
            classes.append(cls)

            assoc = TeacherClassAssociation(teacher_id=teacher.id, class_id=cls.id, role=TeacherRole.MAIN)
            db.session.add(assoc)

        today = date.today()
        for i in range(4):  
            session = ClassSession(
                class_id=classes[i].id,
                date=today,
                period_id=period[i].id
            )
            db.session.add(session)

        db.session.commit()
        return jsonify({"message": "Test data populated successfully."})
    

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Finish adding population route!! 


@views.route('/populate-test-data')
def populate_test_data():
    try:
        # 1. Create a teacher
        teacher = Teacher(
            name="John Doe",
            email="johndoe@example.com",
            password="password123",
            gender="Male",
            phone_number=1234567890,
            address="123 Example Street"
        )
        db.session.add(teacher)
        db.session.flush()  # So teacher.id is available

        # 2. Create 6 classes
        subjects = ["Math", "Science", "History", "English", "Geography", "Art"]
        classes = []
        for i, subject in enumerate(subjects):
            cls = Class(year=2025, subject=subject, code=f"{subject[:3].upper()}101")
            db.session.add(cls)
            db.session.flush()
            classes.append(cls)

            # Associate each class with the teacher as MAIN
            assoc = TeacherClassAssociation(teacher_id=teacher.id, class_id=cls.id, role=TeacherRole.MAIN)
            db.session.add(assoc)

        # 3. Create 5 periods
        period_times = [
            ("P1", time(9, 0), time(9, 50)),
            ("P2", time(10, 0), time(10, 50)),
            ("P3", time(11, 0), time(11, 50)),
            ("P4", time(13, 0), time(13, 50)),
            ("P5", time(14, 0), time(14, 50))
        ]

        periods = []
        for code, start, end in period_times:
            p = Period(code=code, start_time=start, end_time=end)
            db.session.add(p)
            db.session.flush()
            periods.append(p)

        # 4. Create class sessions for today, assigning each class to one period
        today = date.today()
        for i in range(5):  # First 5 classes only
            session = ClassSession(
                class_id=classes[i].id,
                date=today,
                period_id=periods[i].id
            )
            db.session.add(session)

        db.session.commit()
        return jsonify({"message": "Test data populated successfully."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

'''

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
# Not need atm - But please leave commented for now, for my reference & other db insertions 
'''        
@views.route('AddClassSession')
def AddClassSession():
    cls = Class.query.get(1)
    cls.schedule = "Mon 09:00,Wed 11:00"
    db.session.commit()

    from iris.utils.schedule_utils import generate_class_sessions_from_class

    sessions = generate_class_sessions_from_class(cls, date(2025, 9, 1), date(2025, 12, 20))
    db.session.add_all(sessions)
    db.session.commit()

@views.route('/api/schedule/<string:user_type>/<int:user_id>')
def schedule_api(user_type, user_id):
    today = date.today()

    if user_type == "student":
        user = Student.query.get_or_404(user_id)
    elif user_type == "teacher":
        user = Teacher.query.get_or_404(user_id)
    else:
        abort(400, description="Invalid user type")

    schedule = user.get_weekly_schedule(today)
    return jsonify(schedule)

