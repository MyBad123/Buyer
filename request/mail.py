import smtplib
import datetime

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

        msg = EmailMessage()
        msg.set_content(self.text)

        msg['Subject'] = 'Заявка [' + subject_number + ']'
        msg['From'] = "gena.kuznetsov@internet.ru"
        msg['To'] = mail

        server = smtplib.SMTP('smtp.mail.ru: 25')
        server.starttls()
        server.login("gena.kuznetsov@internet.ru", "N990kdJXnnY58aKjsMb7")
        server.send_message(msg)
        server.quit()

    def send_mails(self, mails, user):
        """send text to mails"""

        for i in mails:
            # work with message models and get number
            message_object = MessageModel.objects.create(
                user=user,
                mail=i.get('mail'),
                datetime=datetime.datetime.now(),
                route='from',
                message=self.text,
                request=RequestModel.objects.get(id=int(self.request_id))
            )
            number = str(message_object.id) + '-' + str(user.id)

            message_object.number = number
            message_object.save()

            # send message
            self.send_mail(i, number)
