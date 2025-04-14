import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    text,
    Text,
    JSON
)

# from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext
from sqlalchemy.orm import Session, relationship
from typing import Optional, List
from .recruitment import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """User 테이블에 대한 모델"""

    __tablename__ = "users"
    __table_args__ = {
        "schema": "recruitment",
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
    }

    id = Column(String(56), primary_key=True)
    hashed_password = Column(String(128), nullable=False)
    thread_id_assistant = Column(String(64), nullable=True)
    thread_id_job_recommend = Column(String(64), nullable=True)
    thread_id_recruit_recommend = Column(String(64), nullable=True)
    thread_id_roadmap = Column(String(64), nullable=True)
    thread_id_resume_review = Column(String(64), nullable=True)
    thread_id_find_study = Column(String(64), nullable=True)
    vector_store_id = Column(String(64), nullable=True)
    user_img = Column(Text, nullable=True)
    wanted_position = Column(String(256), nullable=True)
    resume_file = Column(Text, nullable=True)

    # 역참조 관계 설정 (필수는 아님)
    table_resumes = relationship("Resume", back_populates="table_users",
                                cascade="all, delete-orphan")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password):
        self.hashed_password = pwd_context.hash(plain_password)

    def __repr__(self):
        return f"<User(id={self.id}, wanted_position={self.wanted_position})>"


def create_user(
    db: Session,
    user_id: str,
    password: str,
    thread_id_assistant: str = None,
    thread_id_job_recommend: str = None,
    thread_id_recruit_recommend: str = None,
    thread_id_roadmap: str = None,
    thread_id_resume_review: str = None,
    thread_id_find_study: str = None,
    vector_store_id: str = None,
    user_img: str = None,
    wanted_position: str = None,
    resume_file: str = None,
):
    user = User(
        id=user_id,
        thread_id_assistant=thread_id_assistant,
        thread_id_job_recommend=thread_id_job_recommend,
        thread_id_recruit_recommend=thread_id_recruit_recommend,
        thread_id_roadmap=thread_id_roadmap,
        thread_id_resume_review=thread_id_resume_review,
        thread_id_find_study=thread_id_find_study,
        vector_store_id=vector_store_id,
        user_img=user_img,
        wanted_position=wanted_position,
        resume_file=resume_file,
    )
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def update_user(
    db: Session,
    user_id: str,
    password: Optional[str] = None,
    thread_id_assistant: Optional[str] = None,
    thread_id_job_recommend: Optional[str] = None,
    thread_id_recruit_recommend: Optional[str] = None,
    thread_id_roadmap: Optional[str] = None,
    thread_id_resume_review: Optional[str] = None,
    thread_id_find_study: Optional[str] = None,
    vector_store_id: Optional[str] = None,
    user_img: Optional[str] = None,
    wanted_position: Optional[str] = None,
    resume_file: Optional[str] = None,
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None  # 또는 raise 예외 처리

    updates = {
        "thread_id_assistant": thread_id_assistant,
        "thread_id_job_recommend": thread_id_job_recommend,
        "thread_id_recruit_recommend": thread_id_recruit_recommend,
        "thread_id_roadmap": thread_id_roadmap,
        "thread_id_resume_review": thread_id_resume_review,
        "thread_id_find_study": thread_id_find_study,
        "vector_store_id": vector_store_id,
        "user_img": user_img,
        "wanted_position": wanted_position,
        "resume_file": resume_file,
    }

    for field, value in updates.items():
        if value is not None:
            setattr(user, field, value)

    if password:
        user.set_password(password)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


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
