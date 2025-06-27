from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, request, abort, send_file
from datetime import datetime, date, timedelta, time
from flask_login import current_user, login_required
from .models import notice, Class, Student, Teacher, ClassSession, Period, TeacherClassAssociation, TeacherRole, User, Pastoral, Award, Flags, StudentCaregiverAssociation, Caregiver
from . import db
from collections import defaultdict
import re
from io import BytesIO

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

# Above methods used for landing pages displaying subjects/classes

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

def getCaregiverDetails(student_id):

    caregiverDetails = db.session.query(Caregiver, StudentCaregiverAssociation.relationship)\
        .join(StudentCaregiverAssociation, Caregiver.id == StudentCaregiverAssociation.caregiver_id)\
        .filter(StudentCaregiverAssociation.student_id == student_id)\
        .all()
    
    return caregiverDetails  

def getStudentDetails(student_id):
    studentDetails = Student.query.filter(Student.id == student_id).first()

    if studentDetails:
        if studentDetails.dob == '' or studentDetails.dob == ' ':
            studentDetails.dob = None

    return studentDetails

@views.route('/student_profile_image/<int:student_id>')
def getStudentProfileImage(student_id):

    student = Student.query.get(student_id)
    if not student or not student.profile:
        #Returning a default image if not profile image exists
        return send_file('static/images/icons/whiteIrisLogo.png')
    
    return send_file(
        BytesIO(student.profile),
        mimetype='image/jpeg',
        as_attachment=False
    )

@views.route('/studentProfile/<int:student_id>')
def studentProfile(student_id):

    profileImage = getStudentProfileImage(student_id)

    caregivers = getCaregiverDetails(student_id)

    studentDetails = getStudentDetails(student_id)
    if studentDetails:
        print(f"DOB value: '{studentDetails.dob}', type: {type(studentDetails.dob)}")

    allFlags = Flags.query.filter_by(student_id=student_id).all() # Getting all flags associated with user

    #Getting pastoral reports for this specific student only
    all_reports = Pastoral.query.filter_by(student_id=student_id).order_by(Pastoral.date.desc()).all()
    
    #Separating merit and incident reports
    merit_reports = [report for report in all_reports if report.reportType == 'Merit']
    incident_reports = [report for report in all_reports if report.reportType == 'Incident']
    
    #Getting awards for the specific student
    allAwards = Award.query.filter_by(student_id=student_id).all()

    #Grouping awards by year
    awardsByYear = defaultdict(list)
    for award in allAwards:
        awardsByYear[award.year].append(award)

    #Converting to regular dict and sorting by year from newest to oldest
    awardsByYear = dict(sorted(awardsByYear.items(), key=lambda x: x[0], reverse=True))

    return render_template('student.html', student_id=student_id, meritReports=merit_reports, incidentReports=incident_reports, pastoral=None, allAwards=allAwards, awardsByYear=awardsByYear, user=current_user, allFlags=allFlags, caregivers=caregivers, studentDetails=studentDetails, profileImage=profileImage)

@views.route('/searchStudent')
def searchstudent():
    return render_template('showstudent.html')

@views.route('/communication')
def communicationC():
    return render_template('communicationcenter.html',user=current_user)

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
    return render_template("attendanceLanding.html", user=current_user, currentDate=currentDate, myClasses = myClasses, otherClasses = otherClasses)

@views.route('/takeAttendance')
def takeAttendance():
    currentDate = datetime.now().date()
    return render_template("takeAttendance.html", user=current_user, currentDate=currentDate)


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
    return render_template('notice.html', allNotices=allNotices, user=current_user)

@views.route('/createNotice', methods=['GET', 'POST'])
def createNotice():
   if request.method == 'POST':
       
       #Creating new notice
       newNotice = notice( 
        title=request.form.get("title"),
        note=request.form.get("note"),
        author=current_user.id #Setting the author of the notice to the current user
        )
       db.session.add(newNotice) #Adding new notice to the database
       db.session.commit() #Committing new notice to the database

       #Flash message to show that the notice has been created
       #flash("Notice Created!", category="success")
       return redirect(url_for('views.viewNotice')) #Takes user back to the notice page
   return render_template("createNotice.html", user=current_user)

@views.route("/editNotice/<int:id>", methods=["GET", "POST"])
def editNotice(id):
    noticeToEdit = notice.query.get(id) #Reading the notice to be edited
    #Checking if the current user is the aithor of the notice
    if noticeToEdit.author != current_user.id:
        flash("You are not authorized to edit this notice.", category="error")
        return redirect(url_for("views.viewNotice")) #Takes user back to the notice page
    
    if request.method == "POST":
        #Updating the notice
        noticeToEdit.title = request.form.get("title")
        noticeToEdit.note = request.form.get("note")
        db.session.commit() #Committing the changes to the database
        #flash("Notice Updated!", category="success") #Flashing success mesasage
        return redirect(url_for("views.viewNotice")) #Takes user back to the notice page
    
    return render_template("editNotice.html", notices=noticeToEdit, user=current_user) 

@views.route('/deleteNotice', methods=['POST'])
def deleteNotice():
    noitceID = request.form.get("id")
    noticeToDelete = notice.query.get(noitceID) #Reading the notice to be deleted

    #Checking if the current user is the author of the notice
    if noticeToDelete and noticeToDelete.author == current_user.id:
        db.session.delete(noticeToDelete) #Deleting the notice from the database
        db.session.commit() #Committing the changes to the database
        #flash("Notice deleted!", category="success") #Flashing success message
    else:
        flash("You are not authorized to delete this notice.", category="error") #User can only delete their own notices
    return redirect("/notice")

@views.route('yourNotices')
def yourNotices():
    userNotices = notice.query.filter_by(author=current_user.id).all() #Reading all the notices created by the user
    return render_template('notice.html', allNotices=userNotices, user=current_user, showOnlyUserNotices=True)

@views.route('/pastoral/<int:student_id>')#Display pastoral reports for a specific student
def pastoral_reports(student_id):
    
    #Getting all the reports for the student
    all_reports = Pastoral.query.filter_by(student_id=student_id).order_by(Pastoral.date.desc()).all()

    #Separating merit and incident reports
    merit_reports = [report for report in all_reports if report.reportType == 'Merit']
    incident_reports = [report for report in all_reports if report.reportType == 'Incident']

    return render_template('pastoral.html', 
                         student_id=student_id, 
                         meritReports=merit_reports,      
                         incidentReports=incident_reports)

@views.route('/add_pastoral_report', methods=['POST'])#Adding a new pastoral report
def add_pastoral_report():
    
    #Getting the form data
    student_id = request.form.get('student_id')
    report_type = request.form.get('report_type')  #Merit or Incident
    
    #Validating required fields
    if not student_id or not report_type:
        flash("Missing required fields!", category="error")
        return redirect(url_for('views.pastoral_reports', student_id=student_id or 1))
    
    #Creating a new report
    new_report = Pastoral(
        reportType=report_type,
        student_id=int(student_id),
        author=request.form.get('author', ''),
        note=request.form.get('description', ''),
        date=request.form.get('date', ''),
        time=request.form.get('time', ''),
        location=request.form.get('location', ''),
        studentsInvolved=request.form.get('studentsInvolved', ''),
        staffInvolved=request.form.get('staffInvolved', ''),
        titleType=request.form.get('type', ''),
    )

    #Additional fields only for incident reports
    if report_type == 'Incident':
        new_report.parentCommunication = request.form.get('parentCommunication', '')
        new_report.disciplinaryActions = request.form.get('disciplinaryActions', '')
        new_report.resolutionStatus = request.form.get('resolutionStatus', '')

    try:
        #Adding and committing to the database
        db.session.add(new_report)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Error adding report!", category="error")
    
    return redirect(url_for('views.pastoral_reports', student_id=student_id))

@views.route('/get_report/<int:report_id>')#Get a specific report by ID for viewing
def get_report(report_id):
    
    report = Pastoral.query.get_or_404(report_id)
    return jsonify({
        'id': report.id,
        'author': report.author,
        'date': report.date,
        'time': report.time,
        'location': report.location,
        'reportType': report.reportType,
        'studentsInvolved': report.studentsInvolved,
        'staffInvolved': report.staffInvolved,
        'note': report.note,
        'titleType': report.titleType,
        'parentCommunication': report.parentCommunication,
        'disciplinaryActions': report.disciplinaryActions,
        'resolutionStatus': report.resolutionStatus
    })

@views.route('/filter_reports/<int:student_id>')#Filter reports by type or title
def filter_reports(student_id):

    filter_type = request.args.get('filterType')  #Merit or Incident
    title_filter = request.args.get('titleFilter')  #teamwork or respect
    sort_by = request.args.get('sortBy', 'latest')

    #Base query filtered by student
    query = Pastoral.query.filter_by(student_id=student_id)

    #Applying filters when provided
    if filter_type:
        query = query.filter_by(reportType=filter_type)

    if title_filter:
        query = query.filter_by(titleType=title_filter)

    #Applying sorting with latest/oldest options
    if sort_by == 'latest':
        reports = query.order_by(Pastoral.date.asc()).all()
    elif sort_by == 'oldest':
        reports = query.order_by(Pastoral.date.desc()).all()
    else:
        #Setting default to latest
        reports = query.order_by(Pastoral.date.desc()).all()

    #Converting reports to list of dictionaries for JSON response
    reports_data = [{
        'id': report.id,
        'author': report.author,
        'date': report.date,
        'time': report.time,
        'location': report.location,
        'reportType': report.reportType,
        'studentsInvolved': report.studentsInvolved,
        'staffInvolved': report.staffInvolved,
        'note': report.note,
        'titleType': report.titleType,
        'parentCommunication': report.parentCommunication,
        'disciplinaryActions': report.disciplinaryActions,
        'resolutionStatus': report.resolutionStatus
    } for report in reports]

    return jsonify(reports_data)

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

@views.route('/profile_image/<int:user_id>')
def getProfileImage(user_id):
    user = User.query.get(user_id)
    if not user or not user.profile:
        #Returning a default image if not profile image exists
        return send_file('static/images/icons/whiteIrisLogo.png')
    
    return send_file(
        BytesIO(user.profile),
        mimetype='image/jpeg',
        as_attachment=False
    )


# Leaving commented out unless in use, to prevent accidental GET request and database filling error. Please leave here for future db population 

# @views.route('/populate_class_sessions', methods=['GET','POST']) # Re-using route to populate db with class sessions to fill teacher timetables. 
# def populate_class_sessions():

#     # Populating class sessions for the next month (from now, using todays date) based on timetable

#     try:
#         # Get the start date (today) and end date (30 days from now)
#         start_date = date.today()
#         end_date = start_date + timedelta(days=30)
        
#         # Get class IDs by their codes - to populate this mapping
#         class_code_to_id = {}
        
#         # Query all classes and create a mapping from code to ID
#         classes = Class.query.all()
#         for cls in classes:
#             class_code_to_id[cls.code] = cls.id
        
#         # Define the timetable based on class codes
#         timetable = {
#             'monday': {
#                 'P1': ['9SOS1'],
#                 'P2': ['10HIS'],
#                 'P3': [],  # No class
#                 'P4': ['11GEO1'],
#                 'P5': ['9SOS2']
#             },
#             'tuesday': {
#                 'P1': ['12GEO'],
#                 'P2': [],  # No class
#                 'P3': ['11HIS'],
#                 'P4': ['10SOS'],
#                 'P5': ['13GEO']
#             },
#             'wednesday': {
#                 'P1': ['10HIS'],
#                 'P2': ['11GEO1'],
#                 'P3': ['9SOS1'],
#                 'P4': ['11GEO2'],
#                 'P5': []  # No class
#             },
#             'thursday': {
#                 'P1': ['9SOS2'],
#                 'P2': ['12GEO'],
#                 'P3': [],  # No class
#                 'P4': ['11HIS'],
#                 'P5': ['10SOS']
#             },
#             'friday': {
#                 'P1': ['10HIS'],
#                 'P2': [],  # No class
#                 'P3': ['9SOS1'],
#                 'P4': [],  # No class
#                 'P5': ['11GEO2']
#             }
#         }
        
#         # Weekday mapping (Monday = 0, Sunday = 6)
#         weekday_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
#         sessions_created = 0
#         current_date = start_date
        
#         while current_date <= end_date:
#             # Get the day of the week
#             weekday = current_date.weekday()  # 0 = Monday, 6 = Sunday
#             day_name = weekday_names[weekday]
            
#             # Skip weekends 
#             if day_name in ['saturday', 'sunday']:
#                 current_date += timedelta(days=1)
#                 continue
            
#             # Check if this day has classes scheduled
#             if day_name in timetable:
#                 daily_schedule = timetable[day_name]
                
#                 # Iterate through each period for this day
#                 for period_code, class_codes in daily_schedule.items():
#                     # Skip empty periods
#                     if not class_codes:
#                         continue
                        
#                     # Get the period object
#                     period = Period.query.filter_by(code=period_code).first()
#                     if not period:
#                         continue
                    
#                     # Create sessions for each class in this period
#                     for class_code in class_codes:
#                         # Get the class ID from the mapping
#                         class_id = class_code_to_id.get(class_code)
#                         if not class_id:
#                             print(f"Warning: Class code '{class_code}' not found in database")
#                             continue
                        
#                         # Check if session already exists
#                         existing_session = ClassSession.query.filter_by(
#                             class_id=class_id,
#                             date=current_date,
#                             period_id=period.id
#                         ).first()
                        
#                         if not existing_session:
#                             new_session = ClassSession(
#                                 class_id=class_id,
#                                 date=current_date,
#                                 period_id=period.id
#                             )
#                             db.session.add(new_session)
#                             sessions_created += 1
            
#             current_date += timedelta(days=1)
        
#         # Commit all changes
#         db.session.commit()
        
#         return jsonify({
#             'success': True,
#             'message': f'Successfully created {sessions_created} class sessions',
#             'sessions_created': sessions_created,
#             'date_range': f'{start_date} to {end_date}'
#         }), 200
        
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500

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

