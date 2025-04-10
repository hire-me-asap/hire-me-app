
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, text, Text
from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext
from sqlalchemy.orm import Session

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
    thread_id_job_recommend = Column(String(64), nullable=True)
    thread_id_recruit_recommend = Column(String(64), nullable=True)
    thread_id_roadmap = Column(String(64), nullable=True)
    thread_id_resume_review = Column(String(64), nullable=True)
    thread_id_find_study = Column(String(64), nullable=True)
    vector_store_id = Column(String(64), nullable=True)
    user_img = Column(Text, nullable=True)
    wanted_position = Column(String(255), nullable=True)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password):
        self.hashed_password = pwd_context.hash(plain_password)

    def __repr__(self):
        return f"<User(id={self.id}, wanted_position={self.wanted_position})>"

def create_user(db: Session, user_id: str, password: str,
                thread_id_job_recommend: str = None, thread_id_recruit_recommend: str = None, thread_id_roadmap: str = None, thread_id_resume_review: str = None, thread_id_find_study: str = None, vector_store_id: str = None,
                user_img: str = None, wanted_position: str = None):
    user = User(
    id=user_id,
    thread_id_job_recommend=thread_id_job_recommend,
    thread_id_recruit_recommend=thread_id_recruit_recommend,
    thread_id_roadmap=thread_id_roadmap,
    thread_id_resume_review=thread_id_resume_review,
    thread_id_find_study=thread_id_find_study,
    vector_store_id=vector_store_id,
    user_img=user_img,
    wanted_position=wanted_position,
)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

# 1. user_id 로 조회
def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

# # 2. 전체 유저 조회 
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()

# # 3. thread_id 로 조회
# def get_user_by_thread_id(db: Session, thread_id: str):
#     return db.query(User).filter(User.thread_id == thread_id).first()

# # 4. vector_store_id 로 조회
# def get_user_by_vector_store_id(db: Session, vector_store_id: str):
#     return db.query(User).filter(User.vector_store_id == vector_store_id).first()

# # 5. wanted_position 으로 조회 (여러 명 나올 수 있어서 .all())
# def get_users_by_wanted_position(db: Session, wanted_position: str):
#     return db.query(User).filter(User.wanted_position == wanted_position).all()

# # 6. study_thread_id 로 조회
# def get_users_by_study_thread_id(db: Session, study_thread_id: str):
#     return db.query(User).filter(User.study_thread_id == study_thread_id).all()

# # 7. user_img 로 조회 (이미지 있는 유저 찾기)
# def get_users_by_user_img(db: Session, user_img: bytes):
#     return db.query(User).filter(User.user_img == user_img).all()     
