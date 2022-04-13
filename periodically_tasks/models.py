from sqlalchemy import (
    Table, Column, MetaData, DateTime,
    Integer, String, ForeignKey
)


metadata_obj = MetaData()

user_table = Table(
    'auth_user', 
    metadata_obj,
    Column('id', Integer, primary_key=True)
)

request_table = Table(
    'requests', 
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('words', String),
    Column('datetime_created', DateTime),
    Column('datetime_google_started', DateTime),
    Column('datetime_google_finished', DateTime),
    Column('datetime_yandex_started', DateTime),
    Column('datetime_yandex_finished', DateTime),
    Column('datetime_site_parsing_started', DateTime),
    Column('datetime_processing_finished', DateTime), 
    Column('user_id', ForeignKey('auth_user.id'), nullable=False)
)

messages_table = Table(
    'messages',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('mail', String),
    Column('datetime', DateTime),
    Column('route', String),
    Column('message', String),
    Column('number', String),
    Column('request_id', ForeignKey('requests.id'), nullable=False),
    Column('user_id', ForeignKey('auth_user.id'), nullable=False)
)

waiting_messages_table = Table(
    'auth_user', 
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('number', String),
    Column('datetime', DateTime)
)



