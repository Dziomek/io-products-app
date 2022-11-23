from flask import jsonify, request
from . import app
from flask_jwt_extended import create_access_token
from .models import db, User

@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({"data": ["data1", "data2", "data3"]})

    return response


@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token": access_token}
    return response


@app.route('/register_user', methods=['POST'])
def register_user():
    email = request.json.get("email")
    password = request.json.get("password")
    if email and password:
        user = User(username='User', email=email, password=password)
        db.session.add(user)
        db.session.commit()
        response = {"message": "User succesfully created"}
        return response

    return {"message": "Something went wrong. Please try again"}