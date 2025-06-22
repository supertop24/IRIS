from flask import jsonify, Blueprint, request,send_file
from website.sqlite_helper import get_db
from datetime import date
import io
command = Blueprint('command', __name__)

@command.route('/search', methods=['GET'])
def search_student():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    search_pattern = f"%{query}%"
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT user.id, user.name
            FROM user
            WHERE user.role = 'student' AND user.name LIKE ?;
        """,
            (search_pattern,),
        )
        results = cursor.fetchall()

        user = []
        for row in results:
            id,name= row
            user.append(
                {
                    "name": name,
                    "id": id,
                }
            )

        return jsonify(user)

    except Exception as ex:
        return jsonify({"error": "Internal server error"}), 500

@command.route('/searchUser', methods=['GET'])
def search_user():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    search_pattern = f"%{query}%"
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT user.id, user.name
            FROM user
            WHERE user.name LIKE ?;
        """,
            (search_pattern,),
        )
        results = cursor.fetchall()

        user = []
        for row in results:
            id,name= row
            user.append(
                {
                    "name": name,
                    "id": id,
                }
            )

        return jsonify(user)

    except Exception as ex:
        return jsonify({"error": "Internal server error"}), 500
    
@command.route('/searchID', methods=['GET'])
def search_by_id():
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"error": "No ID provided"}), 400

    try:
        user_id = int(user_id)  # 🔒 ensure it's an int
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT name, address
            FROM user
            WHERE id = ?;
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            name, address = row
            return jsonify({
                "name": name,
                "address": address
            })
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@command.route('/uploadReport',methods=['POST'])
def upload():
    report_type = request.form.get('type')
    report_grade = request.form.get('grade')
    report_student_id = request.form.get('student_id')
    report_teacher_id = request.form.get('teacher_id')
    report_note = request.form.get('note')
    report_created_at = date.today().isoformat()
    report_file = request.files.get('pdf')
    try:
        file_data = report_file.read()
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO report (type, grade, student_id, teacher_id, note, created_at,file)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, 
        (
            report_type,
            report_grade,
            report_student_id,
            report_teacher_id,
            report_note,
            report_created_at,
            file_data
        ))
        db.commit()
        return jsonify({'status': 'success', 'message': 'Report inserted successfully'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@command.route('/sendMessage',methods=['POST'])
def send():
    sender_id = request.form.get('sender_id')
    sender = request.form.get('sender')
    target_id = request.form.get('target_id')
    target = request.form.get('target')
    message = request.form.get('message')
    created_at = date.today().isoformat()
    try:
        
        db = get_db()
        cursor = db.cursor()
        
        print('test3')
        cursor.execute("""
            INSERT INTO message_log (sender_id, target_id, message,created_at,sender,target)
            VALUES (?, ?, ?, ?, ?, ?)
        """, 
        (
            sender_id,
            target_id,
            message,
            created_at,
            sender,
            target
        ))
        
        print('test1')
        db.commit()
        print('test')
        return jsonify({'status': 'success', 'message': 'Report inserted successfully'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@command.route('/searchFile', methods=['GET'])
def search_file():
    file_id = request.args.get('id')
    print(file_id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT file FROM report WHERE id = ?", (file_id,))
    row = cursor.fetchone()
    if row:
        file_blob = row[0]  # just the file blob
        return send_file(
            io.BytesIO(file_blob),
            mimetype='application/pdf',
            as_attachment=False
        )
    else:
        return {"error": "File not found"}, 404

@command.route('/academic_list', methods=['GET'])
def search_list():
    student_id = request.args.get("id")
    if not student_id:
        return jsonify({"error": "No ID provided"}), 400

    try:
        student_id = int(student_id)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, grade, note, created_at
            FROM report
            WHERE student_id = ?;
        """, (student_id,))
        rows = cursor.fetchall()

        if not rows:
            return jsonify([])  # return empty list if no data

        # Convert rows (tuples) into list of dicts
        result = []
        for row in rows:
            id, year, term, date = row
            result.append({
                "id": id,
                "year": year,
                "term": term,
                "date": date
            })

        return jsonify(result)

    except Exception as e:
        print(e)  # for debugging
        return jsonify({"error": "Internal server error"}), 500
    
@command.route('/message_list', methods=['GET'])
def message_list():
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"error": "No ID provided"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT 
                message_log.message,
                message_log.sender,
                message_log.created_at,
                user.name
            FROM message_log
            JOIN user ON message_log.sender_id = user.id
            WHERE message_log.target_id = ?;
        """, (user_id,))

        rows = cursor.fetchall()

        if not rows:
            return jsonify([])  # return empty list if no data

        # Convert rows (tuples) into list of dicts
        result = []
        for row in rows:
            message, title, date, name = row
            result.append({
                "message": message,
                "title": title,
                "date": date,
                "name": name
            })

        return jsonify(result)

    except Exception as e:
        print(e)  # for debugging
        return jsonify({"error": "Internal server error"}), 500