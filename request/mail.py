import os
import smtplib
import datetime
import pathlib
from dotenv import load_dotenv

from email.message import EmailMessage

from django.core.mail import EmailMessage as EmailMessageDjango

from app.models import (
    MessageModel,
    RequestModel,
)


class Mail:
    """class for send mail"""

    def __init__(self, text, request_id):
        self.text = text
        self.request_id = request_id

    @staticmethod
    def send_email_attach(email: str, file_path: str):
        email = EmailMessageDjango(
            subject='Parsing result',
            from_email='buyer-support@1d61.com',
            to=[email]
        )
        email.attach_file(file_path)
        email.send()

    def send_mail(self, mail, subject_number):
        """send text to mail"""

        print(mail)
        print(subject_number)

        # get env params for access to mails
        dotenv_path = os.path.join(
            str(pathlib.Path(__file__).parent.parent) + '/Buyer',
            '.env'
        )
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        # send mail
        msg = EmailMessage()
        msg.set_content(self.text)

        msg['Subject'] = 'Заявка [' + subject_number + ']'
        msg['From'] = os.environ.get('from', 'buyer-support@1d61.com'),
        msg['To'] = mail

        server = smtplib.SMTP('m.1d61.com: 587')
        server.starttls()
        server.login(
            os.environ.get('from', 'buyer-support@1d61.com'),
            os.environ.get('password', 'AJds38Adj3FSDl3as4')
        )
        server.send_message(msg)
        server.quit()

    def send_mails(self, mails, user):
        """send text to mails"""

        for i in mails:
            # work with message models and get number
            message_object = MessageModel.objects.create(
                datetime=datetime.datetime.now(),
                route='from',
                message=self.text,
                mail=i
            )
            number = str(message_object.id) + '-' + str(user.id)

            message_object.number = number
            message_object.save()

            # send message
            self.send_mail(i.mail, number)
