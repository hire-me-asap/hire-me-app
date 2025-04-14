import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    text,
    Text,
    JSON
)

from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional, List


Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Resume(Base):
    """Resume 테이블에 대한 모델"""

    __tablename__ = "resumes"
    __table_args__ = {
        "schema": "recruitment",
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
    }

    # User 테이블의 id를 기본 키이자 외래 키로 사용
    id = Column(String(50),
                ForeignKey("recruitment.users.id"),
                primary_key=True, index=True)
    # 기술스택
    skill_stack = Column(JSON, nullable=True)  # json이니까 유의!
    # 경력
    work_experiences = Column(Text, nullable=True)
    # 최종학력
    final_degree = Column(String(64), nullable=True)
    # 전공
    major = Column(String(255), nullable=True)
    # 학점
    gpa = Column(Numeric(3, 2), nullable=True)
    # 교육 및 기타경험
    education_and_exp = Column(String(255), nullable=True)
    # 자격증, 수상내역, 언어, 기타 정보
    certificates = Column(Text, nullable=True)
    awards = Column(Text, nullable=True)
    languages = Column(String(255), nullable=True)
    additional_info = Column(Text, nullable=True)

    # from sqlalchemy.orm import relationship
    # User와의 관계 설정 - 양방향 참조를 위해 수정
    # user = relationship("User", back_populates="resume")


'''
# gpt가 json을 추천함
educations = Column(JSON, nullable=True)  # 여러 교육 정보를 구조화하여 저장
experiences = Column(JSON, nullable=True)  # 경험 정보를 구조화하여 저장
awards = Column(JSON, nullable=True)  # 수상 정보를 구조화하여 저장
languages = Column(JSON, nullable=True)  # 언어 정보를 구조화하여 저장
certificates = Column(JSON, nullable=True)  # 자격증 정보를 구조화하여 저장
'''


def create_resume(
    db: Session,
    user_id: str,
    skill_stack: str = None,  # json이어야 하나?
    work_experiences: str = None,
    final_degree: str = None,
    major: str = None,
    gpa: float = None,  # 위는 numeric인데 여기는 python이니까 float이 맞겠지?
    education_and_exp: str = None,
    certificates: str = None,
    awards: str = None,
    languages: str = None,
    additional_info: str = None,
):

    resume = Resume(
        id=user_id,
        skill_stack=skill_stack,
        work_experiences=work_experiences,
        final_degree=final_degree,
        major=major,
        gpa=gpa,
        education_and_exp=education_and_exp,
        certificates=certificates,
        awards=awards,
        languages=languages,
        additional_info=additional_info
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_resume_by_id(db: Session, user_id: str):
    return db.query(Resume).filter(Resume.id == user_id).first()


def update_resume(
    db: Session,
    user_id: str,
    skill_stack: Optional[List[float]] = None,
    work_experiences: Optional[str] = None,
    final_degree: Optional[str] = None,
    major: Optional[str] = None,
    gpa: Optional[str] = None,
    education_and_exp: Optional[str] = None,
    certificates: Optional[str] = None,
    awards: Optional[str] = None,
    languages: Optional[str] = None,
    additional_info: Optional[str] = None
):

    resume = db.query(Resume).filter(Resume.id == user_id).first()
    if not resume:
        return None  # 또는 raise 예외 처리

    updates = {
        "skill_stack": skill_stack,
        "work_experiences": work_experiences,
        "final_degree": final_degree,
        "major": major,
        "gpa": gpa,
        "education_and_exp": education_and_exp,
        "certificates": certificates,
        "awards": awards,
        "languages": languages,
        "additional_info": additional_info
    }

    for field, value in updates.items():
        if value is not None:
            setattr(resume, field, value)

    db.commit()
    db.refresh(resume)
    return resume


def delete_resume(db: Session, user_id: str):
    resume = db.query(Resume).filter(Resume.id == user_id).first()
    if resume:
        db.delete(resume)
        db.commit()
        return True
    return False
