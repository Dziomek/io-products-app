import re
from itsdangerous import URLSafeTimedSerializer


def email_check(email):
    return re.fullmatch("[^@]+@[^@]+\.[^@]+", email)


def password_check(password, confirm_password):
    return password == confirm_password


def email_verification_token(email):
    s = URLSafeTimedSerializer('Thisisasecret!')
    token = s.dumps(email, salt='SALT')
    return token
