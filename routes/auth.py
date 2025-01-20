from flask import Blueprint, request, jsonify
from hashlib import sha256
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    username = data['username']
    if Users.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = Users(
        username=username,
        password=hashed_password,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Users.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.username)
    return jsonify({"token": access_token}), 200
