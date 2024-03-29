from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader
from flask_backend import app
import os

EMAIL_ADDRESS = app.config["EMAIL_ADDRESS"]
EMAIL_PASSWORD = app.config["EMAIL_PASSWORD"]

# This class build as Singleton is responsible for sending email verifications
class MailService:

    smtpObj = smtplib.SMTP("smtp.gmail.com")
    #smtpObj.ehlo()
    smtpObj.connect("smtp.gmail.com", "587")
    smtpObj.starttls()
    smtpObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # This method sends the verification link for a new user
    @staticmethod
    def sendVerificationLink(link, emailUser, username):
        msg = EmailMessage()
        msg['Subject'] = f'Verification Link'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = emailUser

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        file_loader = FileSystemLoader(template_dir)
        env = Environment(loader=file_loader)
        template = env.get_template('email_verification.html')
        output = template.render(link=link, username=username)
        msg.add_alternative(output, subtype='html')

        MailService.smtpObj.send_message(msg)
