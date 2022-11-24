from flask import jsonify, request
from flask_login import login_user, logout_user
from . import app
from flask_jwt_extended import create_access_token
from .models import db, User
from flask_bcrypt import generate_password_hash, check_password_hash
from .utils import email_check, password_check

@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({"data": ["data1", "data2", "data3"]})

    return response


@app.route('/token', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            access_token = create_access_token(identity=email)
            response = {
                "access_token": access_token,
                "username": user.username}
            return response


@app.route('/register_user', methods=['POST'])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    confirm_password = request.json.get("confirmPassword")

    if not (username and email and password and confirm_password):
        return {"message": "Missing fields. Please try again"}
    user = User.query.filter_by(username=username).first()
    if user:
        return {"message": "User with this username already exists"}
    user = User.query.filter_by(email=email).first()
    if user:
        return {"message": "User with this email already exists"}
    if not email_check(email):
        return {"message": "Invalid email address. Please try again"}
    if not password_check(password, confirm_password):
        return {"message": "Passwords don't match. Please try again"}

    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password, is_active=True)
    db.session.add(user)
    db.session.commit()
    return {"message": "User succesfully created"}


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return {"message": "user logged out"}