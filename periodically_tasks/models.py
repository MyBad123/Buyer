from sqlalchemy import (
    Table, Column, MetaData, DateTime,
    Integer, String, Text
)


metadata_obj = MetaData()

MessageModel = Table(
    'messages',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('datetime', DateTime),
    Column('route', String(300)),
    Column('message', Text),
    Column('number', String(300)),
    Column('mail_id', Integer),
)


ParsingAttributesTable = Table(
    'mail_hendler',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(300)),
    Column('value', String(300)),
    Column('message_id', Integer),
)
