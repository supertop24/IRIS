from flask import jsonify, Blueprint, request
from website.db import get_db
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
        print(f"DB object: {db}")
        cursor = db.cursor()
        cursor.execute("""
            SELECT name, address
            FROM user
            WHERE id = ?;
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            name, address = row
            print(f"User name: {name}") 
            return jsonify({
                "name": name,
                "address": address
            })
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
