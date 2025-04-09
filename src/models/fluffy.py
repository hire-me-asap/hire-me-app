import os
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Fluffy(Base):
    __tablename__ = 'fluffy'
    __table_args__ = {
        'schema': os.getenv('SQLALCHEMY_DB_NAME'),
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
    }

    fluffy_stuff_name = Column(String(40), nullable=False)
    created_date = Column(DateTime, nullable=False,
                          server_default=text('CURRENT_TIMESTAMP'))
    updated_date = Column(DateTime, nullable=True,
                          server_onupdate=text('CURRENT_TIMESTAMP'))

    def __repr__(self):
        return f"<Fluffy(stuff={self.fluffy_stuff_name})>"
