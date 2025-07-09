# auth.py
# from functools import wraps
# from flask import request, jsonify
# from config import API_KEY
# import os

# API_KEY = os.getenv("API_KEY", "AIzaSyB9ThmsotlDkPXcM1tQid57Fz9L5s6t9B8")

# def require_api_key(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if request.headers.get("x-api-key") == API_KEY:
#             return f(*args, **kwargs)
#         return jsonify({"error": "Unauthorized"}), 401
#     return decorated