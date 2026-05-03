from flask import Blueprint, request, jsonify
from auth.models import create_user, find_user_by_email, verify_password
import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET, JWT_EXPIRY_HOURS

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    if find_user_by_email(email):
        return jsonify({"error": "Email already registered"}), 409

    create_user(name, email, password)
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = find_user_by_email(email)
    if not user or not verify_password(password, user.get("password")):
        return jsonify({"error": "Invalid email or password"}), 401

    token = jwt.encode({
        'user_id': str(user.get('_id')),
        'email': user.get('email'),
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }, JWT_SECRET, algorithm='HS256')

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "name": user.get("name"),
            "email": user.get("email"),
            "created_at": user.get("created_at")
        }
    }), 200
