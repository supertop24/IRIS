from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, request, abort
from datetime import datetime, date, timedelta, time
from flask_login import current_user, login_required
from .models import notice, Class, Student, Teacher, ClassSession, Period, TeacherClassAssociation, TeacherRole
from . import db

views = Blueprint('views', '__name__')

@views.route('/')
def portalSelect():
   return render_template("portalSelect.html")

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
   return render_template('dashboard.html', user=current_user, currentDate=currentDate)

# Adding API endpoint for getting teacher schedule data here with the dashboard route, since this is where it'll be used
@views.route('/api/daily-schedule')
@login_required
def api_daily_schedule():
    print("Logged in user:", current_user.id, current_user.__class__.__name__)

    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
    
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error: invalid date format'}), 400

    print("API request date:", selected_date)

    if isinstance(current_user, Student) or isinstance(current_user, Teacher):
        schedule = current_user.get_daily_schedule(selected_date)
    else:
        print("User is not a Teacher or Student.")
        return jsonify([])

    serialized = []
    for s in schedule:
        serialized.append({
            'class_code': s.class_.code,
            'subject': s.class_.subject,
            'period_id': s.period.id if s.period else None,
            'period_label': s.period.label if hasattr(s.period, 'label') else None,
            'date': s.date.isoformat()
        })

    print("Serialized sessions:", serialized)
    return jsonify(serialized)

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
    '''
