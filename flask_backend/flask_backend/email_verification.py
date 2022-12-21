from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader
from flask_backend import app

EMAIL_ADDRESS = app.config["EMAIL_ADDRESS"]
EMAIL_PASSWORD = app.config["EMAIL_PASSWORD"]

#TODO: Mayby a class with only static methods would be better
class MailService:

    def __init__(self):
        #   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as self.smtp:
        #   self.smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        self.smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtpObj.ehlo()
        self.smtpObj.starttls()
        self.smtpObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    def sendVerificationLink(self, link, emailUser, username):
        msg = EmailMessage()
        msg['Subject'] = f'Verification Link'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = emailUser

        file_loader = FileSystemLoader('flask_backend/flask_backend/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('email_verification.html')
        output = template.render(link=link, username=username)
        msg.add_alternative(output, subtype='html')

        self.smtpObj.send_message(msg)