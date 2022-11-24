from flask import jsonify, request
from flask_login import login_user, logout_user
from . import app
from flask_jwt_extended import create_access_token
from .models import db, User
from flask_bcrypt import generate_password_hash, check_password_hash
from .utils import email_check

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
            response = {"access_token": access_token}
            return response


@app.route('/register_user', methods=['POST'])
def register():
    email = request.json.get("email")
    password = request.json.get("password")
    hashed_password = generate_password_hash(password)
    if email_check(email) and password:
        user = User(username='User', email=email, password=hashed_password, is_active=True)
        db.session.add(user)
        db.session.commit()
        response = {"message": "User succesfully created"}
        return response

    return {"message": "Something went wrong. Please try again"}


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return {"message": "user logged out"}