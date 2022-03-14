import smtplib
import datetime

from email.message import EmailMessage
from django.db.utils import IntegrityError

from app.models import (
    MessageModel, MailForMessageModel, 
    WaitingMessages, ResultModel
)


class Mail:
    """class for send mail"""
    
    def __init__(self, text):
        self.text = text

    def send_mail(self, mail, subject_number):
        """send text to mail"""

        msg = EmailMessage()
        msg.set_content(self.text)

        msg['Subject'] = 'Заявка [' + subject_number + ']'
        msg['From'] = "gena.kuznetsov@internet.ru"
        msg['To'] = mail

        server = smtplib.SMTP('smtp.mail.ru: 25')
        server.starttls()
        server.login("gena.kuznetsov@internet.ru", "o%pdUaeIUI12")
        server.send_message(msg)
        server.quit()

    def set_mail_for_chat(self, mail):
        """set mail to db"""

        try:
            MailForMessageModel.objects.create(
                mail=mail
            )
        except IntegrityError:
            pass

    def set_number_for_waiting(self, number):
        """set number to db"""

        WaitingMessages.objects.create(
            number=number,
            datetime=datetime.datetime.now()
        )

    def send_mails(self, mails, user):
        """send text to mails"""

        for i in mails:
            # work with message models and get number
            message_object = MessageModel.objects.create(
                user=user,
                mail=i,
                datetime=datetime.datetime.now(),
                route='from',
                message=self.text, 
                result=ResultModel.objects.all()[0]
            )
            number = str(message_object.id) + '-' + str(user.id)
            
            message_object.number = number
            message_object.save()

            # save some data to db 
            self.set_number_for_waiting(number)

            # send message
            self.send_mail(i, number)