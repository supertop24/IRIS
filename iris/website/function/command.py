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
            SELECT user.name, user.role
            FROM user
            WHERE user.role = 'student' AND user.name LIKE ?;
        """,
            (search_pattern,),
        )
        results = cursor.fetchall()

        user = []
        for row in results:
            name, role = row
            user.append(
                {
                    "name": name,
                    "role": role,
                }
            )

        return jsonify(user)

    except Exception as ex:
        return jsonify({"error": "Internal server error"}), 500
