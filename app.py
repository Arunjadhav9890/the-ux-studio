# app.py
import traceback
from flask import Flask, request, jsonify
from auth import require_api_key
from database import init_db, get_connection
from datetime import datetime

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return "🎓 Welcome to the Student API"

# CREATE
from firebase_setup import db  # 👈 import firestore DB

@app.route('/students', methods=['POST'])
@require_api_key
def add_student():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400

    try:
        # Save to Firebase Firestore
        db.collection("students").add({
            "name": name,
            "email": email,
            "message": message,
            "created_at": created_at
        })

        return jsonify({"message": "Student added to Firebase"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# READ ALL
@app.route('/students', methods=['GET'])
@require_api_key
def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return jsonify([
        {
            "id": s[0],
            "name": s[1],
            "email": s[2],
            "message": s[3],
            "created_at": s[4]
        } for s in data
    ])

# READ ONE
@app.route('/students/<int:id>', methods=['GET'])
@require_api_key
def get_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "message": row[3],
            "created_at": row[4]
        })    
    return jsonify({"error": "Student not found"}), 404

# UPDATE
@app.route('/students/<int:id>', methods=['PUT'])
@require_api_key
def update_student(id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=?, email=?, message=? WHERE id=?",
        (name, email, message, id)
    )    
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated successfully"})

# DELETE
@app.route('/students/<int:id>', methods=['DELETE'])
@require_api_key
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Student with ID {id} deleted successfully"})

if __name__ == '__main__':
    print("🚀 Running at http://127.0.0.1:5000")
    print("🔐 Use x-api-key header with your API key")
    app.run(debug=True)
