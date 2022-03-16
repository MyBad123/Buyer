from sqlalchemy import (
    Table, Column, MetaData, DateTime,
    Integer, String
)


metadata_obj = MetaData()

request_table = Table(
    'requests', 
    metadata_obj,
    Column('id', Integer),
    Column('name', String),
    Column('words', String),
    Column('datetime_created', DateTime),
    Column('datetime_google_started', DateTime),
    Column('datetime_google_finished', DateTime),
    Column('datetime_yandex_started', DateTime),
    Column('datetime_yandex_finished', DateTime),
    Column('datetime_site_parsing_started', DateTime),
    Column('datetime_processing_finished', DateTime)
)

'''
    datetime_google_started = models.DateTimeField(null=True, blank=True)
    datetime_google_finished = models.DateTimeField(null=True, blank=True)
    datetime_yandex_started = models.DateTimeField(null=True, blank=True)
    datetime_yandex_finished = models.DateTimeField(null=True, blank=True)
    datetime_site_parsing_started = models.DateTimeField(null=True, blank=True)
    datetime_processing_finished = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
'''