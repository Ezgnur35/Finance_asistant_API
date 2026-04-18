from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email ve şifre zorunlu"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Bu email zaten kayıtlı"}), 400

    password_hash = generate_password_hash(data["password"])
    user = User(email=data["email"], password_hash=password_hash)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Kayıt başarılı"}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email ve şifre zorunlu"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Email veya şifre hatalı"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token}), 200