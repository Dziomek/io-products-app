import re
from itsdangerous import URLSafeTimedSerializer
from .email_verification import MailService
from flask_backend import app

SECRET = app.config["TOKEN_SECRET"]
SALT = app.config["TOKEN_SALT"]

# This function validates the email string provided as an input
def email_check(email):
    return re.fullmatch("[^@]+@[^@]+\.[^@]+", email)

# This function validates if the passwords are the same
def password_check(password, confirm_password):
    return password == confirm_password

# This function generates the token for email confirmation
def email_verification_token(email):
    s = URLSafeTimedSerializer(SECRET)
    token = s.dumps(email, salt=SALT)
    return token

# This function validates the token for email confirmation
def verify_email(token):
    s = URLSafeTimedSerializer(SECRET)
    return s.loads(token, salt=SALT, max_age=3600)

# This function sends the link by email for user verification
def send_email_with_token(link, email, username):
    m = MailService()
    m.sendVerificationLink(link, email, username)
    return
