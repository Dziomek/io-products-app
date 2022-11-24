import re


def email_check(email):
    return re.fullmatch("[^@]+@[^@]+\.[^@]+", email)


def password_check(password, confirm_password):
    return password == confirm_password
