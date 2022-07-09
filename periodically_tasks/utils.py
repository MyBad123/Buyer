import ssl
import json
import requests
import datetime
from sqlalchemy import (
    select, insert, create_engine
)
import mailparser
from imapclient import IMAPClient

from .models import (
    MessageModel, ParsingAttributesTable
)


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
            + datetime.timedelta(days=-7)

        # make query for get all messages
        query = select(MessageModel) \
            .where(MessageModel.c.datetime > interval) \
            .order_by(MessageModel.c.datetime)

        with self.engine.connect() as conn:
            result = conn.execute(query)

        # work with result of query
        for i in result:
            if (i[2] == 'from'):
                self.number_list.append(i[4])

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
                select_saving = select(MessageModel) \
                    .where(MessageModel.c.number == i)

                with self.engine.connect() as conn:
                    for j in conn.execute(select_saving):
                        model_data = j

                # save to model
                try:
                    insert_query = insert(MessageModel).values(
                        datetime=datetime.datetime.now(),
                        route='to',
                        message=message_data,
                        number=model_data[4],
                        mail_id=model_data[5],
                        see='no'
                    )
                    with self.engine.connect() as conn:
                        after_insert_data = conn.execute(insert_query)

                    # get id for insert parsing data from mail
                    key = after_insert_data.inserted_primary_key[0]

                    # it is parsing
                    mail_hendler_request = requests.post(
                        'http://127.0.0.1:8011/process_text',
                        json=json.dumps({'text': str(message_data)})
                    )
                    data_from_request = mail_hendler_request.json()
                    print(data_from_request)

                    # get data after parsing
                    people = data_from_request.get('people')
                    emails = data_from_request.get('emails')
                    phones = data_from_request.get('phones')
                    sites = data_from_request.get('sites')
                    companies = data_from_request.get('companies')
                    addresses = data_from_request.get('addresses')
                    positions = data_from_request.get('positions')

                    # set data to db
                    with self.engine.connect() as conn:
                        '''
                        for j in people:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='people',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)
                        '''
                        for j in emails:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='emails',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)

                        for j in phones:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='phones',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)

                        for j in sites:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='sites',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)
                        '''
                        for j in companies:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='companies',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)

                        for j in addresses:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='addresses',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)

                        for j in positions:
                            insert_query = insert(ParsingAttributesTable).values(
                                name='positions',
                                value=j,
                                message_id=key
                            )
                            conn.execute(insert_query)
                        '''
                except TypeError:
                    pass

    def work(self):
        """work with mails"""

        HOST = "m.1d61.com"
        USERNAME = "buyer-vendor@1d61.com"
        PASSWORD = "GD38asDF348ASdf"

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
                except SyntaxError:
                    pass

                # delete mail from message
                self.delete_mail(server, uid)


if __name__ == '__main__':
    cls_obj = MessageNumber()
    cls_obj.get_numbers()
    cls_obj.work()
