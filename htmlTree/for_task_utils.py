import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from email.mime.text import MIMEText


class Mail:
    def __init__(self, to, path):
        self.mail_from = os.environ.get('from', 'gena.kuznetsov@internet.ru')
        self.mail_password = os.environ.get('password', 'o%pdUaeIUI12')
        self.to = to
        self.path = path
        self.str_connect = os.environ.get('mail-str', 'smtp.mail.ru: 25')

    def send_start_mail(self):
        """send mail about starting"""

        mailMsg = MIMEMultipart()
        mailMsg['Subject'] = 'заявка'
        mailMessage = 'ваша заявка в обработке'
        mailMsg.attach(MIMEText(mailMessage, 'plain'))
        mailServer = smtplib.SMTP('smtp.mail.ru: 25')
        mailServer.starttls()
        mailServer.login(self.mail_from, self.mail_password)
        mailServer.sendmail(self.mail_from, self.to, mailMsg.as_string())
        mailServer.quit()

    def send_file_mail(self, my_path):
        """send csv file"""

        msg = MIMEMultipart()
        msg['Subject'] = 'csv file'
        msg['To'] = self.to

        mailTo = self.to

        # work with file
        with open(my_path, 'rb') as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(my_path)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(my_path)
            msg.attach(part)

        # send message
        mailServer = smtplib.SMTP(self.str_connect)
        mailServer.starttls()
        mailServer.login(self.mail_from, self.mail_password)
        mailServer.sendmail(self.mail_from, mailTo, msg.as_string())
        mailServer.quit()
