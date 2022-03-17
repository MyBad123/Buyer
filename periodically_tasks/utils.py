from sqlalchemy import (
    select, delete, insert, create_engine
)

from .models import waiting_messages_table


class MessageNumber:
    """work with numbers"""
    def __init__(self):
        
        # create list for work witj it
        self.number_list = []

        # create engine for connect to db 
        engine = create_engine(
            "postgresql+psycopg2://buyer_user:KJNjkjnkerKJNEKRF3456@localhost:5432/b2b",
            isolation_level="READ COMMITTED"
        )

        with engine.connect() as conn:
            
            # get numbers of message (old dele)
            stmt = select(waiting_messages_table)

            for i in conn.execute(stmt):
                self.number_list.append(
                    i[1]
                )

    def delete_number(self):
        """delete number from db"""
        