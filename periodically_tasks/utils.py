import ssl
import datetime
from sqlalchemy import (
    select, insert, create_engine
)
import mailparser
from imapclient import IMAPClient

from models import DataModel


class MessageNumber:
    """work with numbers"""

    def __init__(self):
        self.engine = create_engine(
            "postgresql+psycopg2://buyer_user:KJNjkjnkerKJNEKRF3456@localhost:5432/b2b",
            isolation_level='READ COMMITTED'
        )
        self.number_list = []

    def get_numbers(self):
        """get numbers in number_list"""

        # make datetime for acceptable interval
        interval = datetime.datetime.now() \
            + datetime.timedelta(days=-1)

        # make query for get all messages
        query = select(DataModel) \
            .where(DataModel.c.datetime > interval) \
            .order_by(DataModel.c.datetime)

        with self.engine.connect() as conn:
            result = conn.execute(query)

        # work with result of query
        for i in result:
            if (i[4] == 'from') and (i[6] not in self.number_list):
                self.number_list.append(i[6])
            if i[4] != 'from':
                try:
                    self.number_list.remove(i[6])
                except ValueError:
                    pass

    def delete_mail(self, server, uid):
        """delete mail from box"""

        try:
            server.delete_messages(uid)
        except:
            pass

    def write_to_db(self, message_data, heading):
        """add text of message to db"""

        for i in self.number_list:
            number_template = '[' + i + ']'

            if (number_template in message_data) or (number_template in str(heading)):
                # get data for saving
                print('hz')
                select_saving = select(DataModel) \
                    .where(DataModel.c.number == i)

                with self.engine.connect() as conn:
                    for j in conn.execute(select_saving):
                        model_data = j

                # save to model
                try:
                    insert_query = insert(DataModel).values(
                        user_id=model_data[1],
                        mail=model_data[2],
                        datetime=datetime.datetime.now(),
                        route='to',
                        message=message_data,
                        number=model_data[6],
                        request_id=model_data[7]
                    )
                    with self.engine.connect() as conn:
                        conn.execute(insert_query)
                except TypeError:
                    pass

    def work(self):
        """work with mails"""

        HOST = "imap.mail.ru"
        USERNAME = "gena.kuznetsov@internet.ru"
        PASSWORD = "N990kdJXnnY58aKjsMb7"

        ssl_context = ssl.create_default_context()

        # don't check if certificate hostname doesn't match target hostname
        ssl_context.check_hostname = False

        # don't check if the certificate is trusted by a certificate authority
        ssl_context.verify_mode = ssl.CERT_NONE

        with IMAPClient(HOST, ssl_context=ssl_context) as server:
            server.login(USERNAME, PASSWORD)
            server.select_folder("INBOX", readonly=False)

            messages = server.search()
            for uid, message_data in server.fetch(messages, "RFC822").items():
                # add text to db
                try:
                    text_body = mailparser.parse_from_bytes(message_data[b'RFC822']).text_html[0]
                    self.write_to_db(text_body, mailparser.parse_from_bytes(message_data[b'RFC822']))
                except:
                    pass

                # delete mail from message
                # self.delete_mail(server, uid)


if __name__ == '__main__':
    cls_obj = MessageNumber()
    cls_obj.get_numbers()
    cls_obj.work()
