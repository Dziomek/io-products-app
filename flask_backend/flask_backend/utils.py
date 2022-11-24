import re


def email_check(email):
    return re.fullmatch("[^@]+@[^@]+\.[^@]+", email)