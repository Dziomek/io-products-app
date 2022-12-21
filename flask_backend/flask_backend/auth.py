import hashlib

from flask import jsonify, request, url_for, session, flash
from . import app
from flask_jwt_extended import create_access_token
from .utils import email_check, password_check, email_verification_token, verify_email, send_email_with_token
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from .database_connector import DatabaseConnector

db = DatabaseConnector()

@app.route('/token', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = db.select_from_users_by_email(email)
    if len(user) != 0:
        password_hash = hashlib.sha256(password.encode('utf-8'))
        if password_hash.hexdigest() == user[0][3]:
            session['logged_in'] = True
            session['id'] = user[0][0]
            session['username'] = user[0][1]
            session['email'] = user[0][2]
            session['is_active'] = user[0][4]
            # Redirect to home page
            access_token = create_access_token(identity=email)
            response = {
                "access_token": access_token,
                "username": user[0][1],
                "email": user[0][2],
                "is_active": user[0][4]
            }
            return response


@app.route('/register_user', methods=['POST'])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    confirm_password = request.json.get("confirmPassword")

    if not (username and email and password and confirm_password):
        return {"message": "Missing fields. Please try again"}
    user = db.select_from_users_by_username(username)
    if len(user) != 0:
        return {"message": "User with this username already exists"}
    user = db.select_from_users_by_email(email)
    if len(user) != 0:
        return {"message": "User with this email already exists"}
    if not email_check(email):
        return {"message": "Invalid email address. Please try again"}
    if not password_check(password, confirm_password):
        return {"message": "Passwords don't match. Please try again"}

    #TODO: Change hashing function to something that generates salt itself
    password_hash = hashlib.sha256(password.encode('utf-8'))

    db.insert_into_users(username=username, email=email, password_hash=password_hash.hexdigest(), is_active=False)

    token = email_verification_token(email)
    link = url_for('confirm_email', token=token, email=email, _external=True)
    send_email_with_token(link, email, username)

    return {
        "message": "User succesfully created",
        "email": email
    }


@app.route('/confirm_email/<string:token>/<string:email>', methods=['GET'])
def confirm_email(token, email):
    try:
        verify_email(token)
        db.update_users_account_activation(email)
    except SignatureExpired:
        return {"verified": "False"}
    return {"verified": "True"}

@app.route('/logout', methods=['GET'])
def logout():
    # Remove session data, this will log the user out
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('is_active', None)
    flash('Logged out...')
    return {"message": "user logged out"}