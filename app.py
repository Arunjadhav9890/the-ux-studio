# app.py
import traceback
from flask import Flask, request, jsonify
from datetime import datetime
from firebase_setup import db 
import re

app = Flask(__name__)


@app.route('/')
def home():
    return "🎓 Welcome to the Student API"

# Health Check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Attempt to fetch a document to check Firestore connection
        db.collection("students").limit(1).get()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "unhealthy", "error": str(e)}), 500   
# CREATE
@app.route('/sendmessage', methods=['POST'])
def send_message():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400

    if not re.match(r"^[A-Za-z\s]+$", name):
        return jsonify({"error": "Invalid name format"}), 400

    # Email should match typical email format
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
        return jsonify({"error": "Invalid email format"}), 400
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        doc_ref = db.collection("students")
        new_doc_ref = doc_ref.add({
            "name": name,
            "email": email,
            "message": message,
            "created_at": created_at
        })
        print(f"Document created with ID: {new_doc_ref.index}")
        return jsonify({"message": "Message sent successfully", "created_at": created_at}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

    
# Update message
@app.route('/sendmessage/<doc_id>', methods=['PUT'])
def update_message(doc_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400

    try:
        doc_ref = db.collection("students").document(doc_id)
        if not doc_ref.get().exists:
            return jsonify({"error": "Document not found"}), 404

        doc_ref.update({
            "name": name,
            "email": email,
            "message": message,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return jsonify({"message": "Message updated successfully", "id": doc_id}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# delete_message
@app.route('/sendmessage/<doc_id>', methods=['DELETE'])
# @require_api_key
def delete_message(doc_id):
    try:
        doc_ref = db.collection("students").document(doc_id)
        if not doc_ref.get().exists:
            return jsonify({"error": "Document not found"}), 404

        doc_ref.delete()
        return jsonify({"message": f"Message with ID {doc_id} deleted successfully"}), 200   
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

    
# get_message
@app.route('/sendmessage/<doc_id>', methods=['GET'])
# @require_api_key
def get_message(doc_id):
    try:
        doc_ref = db.collection("students").document(doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({"error": "Document not found"}), 404

        return jsonify(doc.to_dict()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# get_all_messages

if __name__ == '__main__':
    print("🚀 Running at http://127.0.0.1:5000")
    print("🔐 Use x-api-key header with your API key")
    app.run(debug=True)
