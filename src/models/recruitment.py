
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, text, Text
from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class WebSite(enum.Enum):
#     WANTED = 1      # 원티드
#     SARAMIN = 2     # 사람인
#     JOBKOREA = 3    # 잡코리아
#     JOBPLANET = 4   # 잡플래닛
#     INCRUIT = 5     # 인쿠르트
#     LINKEDIN = 6    # 링크드인

# class RecruitSite(Base):
#     '''recruit_site 테이블에 대한 모델'''
#     __tablename__ = 'recruit_site'
#     __table_args__ = {
#         'schema': 'recruitment',
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8',
#         'mysql_collate': 'utf8_general_ci',
#     }
    
#     site_id = Column(Integer, primary_key=True, autoincrement=False)
#     site_name = Column(String(40), nullable=False)
#     active = Column(Boolean, nullable=False, server_default=text('true'))
#     created_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
#     updated_date = Column(DateTime, nullable=True, server_onupdate=text('CURRENT_TIMESTAMP'))
    
#     def __repr__(self):
#         return f"<Site(site_id={self.site_id}, site_name={self.site_name})>"


class User(Base):
    """User 테이블에 대한 모델"""
    __tablename__ = 'users'
    __table_args__ = {
        'schema': 'recruitment',
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
    }

    id = Column(String(50), primary_key=True, index=True)
    hashed_password = Column(String(128), nullable=False)
    thread_id = Column(String(64), nullable=True)
    vector_store_id = Column(String(64), nullable=True)
    user_img = Column(Text, nullable=True)
    wanted_position = Column(String(255), nullable=True)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_pw)

    def set_password(self, plain_password):
        self.hashed_pw = pwd_context.hash(plain_password)

    def __repr__(self):
        return f"<User(id={self.id}, thread_id={self.thread_id})>"