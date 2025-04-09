
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class food(Base):
    '''Hungry 테이블에 대한 모델'''
    __tablename__ = 'food'
    __table_args__ = {
        'schema': 'recruitment',
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
    }
    
    food_id = Column(Integer, primary_key=True, autoincrement=False)
    food_name = Column(String(40), nullable=False)
    food_info = Column(String(40), nullable=False)
    food_cal = Column(Integer, nullable=False)
    food_rename = Column(Integer, nullable=True)
    gone = Column(Boolean, nullable=False, server_default=text('true'))
    make_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    def __repr__(self):
        return f"<Site(food_id={self.food_id}, food_name={self.food_name})>"
