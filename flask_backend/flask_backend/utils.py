import re
from itsdangerous import URLSafeTimedSerializer
from .email_verification import MailService


def email_check(email):
    return re.fullmatch("[^@]+@[^@]+\.[^@]+", email)


def password_check(password, confirm_password):
    return password == confirm_password


def email_verification_token(email):
    s = URLSafeTimedSerializer('Thisisasecret!')
    token = s.dumps(email, salt='SALT')
    return token


def verify_email(token):
    s = URLSafeTimedSerializer('Thisisasecret!')
    return s.loads(token, salt='SALT', max_age=3600)


def send_email_with_token(link, email, username):
    m = MailService()
    m.sendVerificationLink(link, email, username)
    return
