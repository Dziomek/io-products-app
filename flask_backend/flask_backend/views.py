import hashlib

from flask import jsonify, request, url_for
from flask_login import login_user, logout_user
from . import app
from . import email_verification
from flask_jwt_extended import create_access_token
from flask_bcrypt import generate_password_hash, check_password_hash
from .utils import email_check, password_check, email_verification_token, verify_email, send_email_with_token
from .email_verification import MailService
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from .database_connector import DatabaseConnector

db = DatabaseConnector()

@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({"data": ["data1", "data2", "data3"]})
    return response

