import datetime
from sqlalchemy import (
    select, delete, insert, create_engine
)
import mailparser
from imapclient import IMAPClient

from .models import DataModel


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
            if (i[4] != 'from'):
                self.number_list.remove(i[6])

    def delete_mail(self, server, uid):
        """delete mail from box"""

        try:
            server.delete_messages(uid)
        except:
            pass

    def write_to_db(self, server, message_data):
        """add text of message to db"""

        for i in self.number_list:
            number_template = '[' \
                + i + ']'

            text = mailparser.parse_from_bytes(message_data[b'RFC822']).text_html[0]

            if number_template in text:


    def work(self):
        """work with mails"""

        HOST = "imap.mail.ru"
        USERNAME = "gena.kuznetsov@internet.ru"
        PASSWORD = "N990kdJXnnY58aKjsMb7"

        with IMAPClient(HOST) as server:
            server.login(USERNAME, PASSWORD)
            server.select_folder("INBOX", readonly=False)

            messages = server.search()
            for uid, message_data in server.fetch(messages, "RFC822").items():
                # add text to db
                try:
                    mailparser.parse_from_bytes(message_data[b'RFC822']).text_html[0]
                except:
                    pass

                # delete mail from message
                self.delete_mail(server, uid)