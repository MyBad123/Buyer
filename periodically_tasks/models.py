from sqlalchemy import (
    Table, Column, MetaData, DateTime,
    Integer, String, ForeignKey, Text
)


metadata_obj = MetaData()

DataModel = Table(
    'messages',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('mail', String(300)),
    Column('datetime', DateTime),
    Column('route', String(50)),
    Column('message', Text),
    Column('number', String(100)),
    Column('request_id', Integer)
)
