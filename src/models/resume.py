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

from typing import Optional, List
from sqlalchemy.orm import Session, relationship
from .recruitment import Base


class Resume(Base):
    """
    Resume 테이블에 대한 모델

    gpt가 아래와 같이 json을 추천함
    educations = Column(JSON, nullable=True)  # 여러 교육 정보를 구조화하여 저장\n
    experiences = Column(JSON, nullable=True)  # 경험 정보를 구조화하여 저장\n
    awards = Column(JSON, nullable=True)  # 수상 정보를 구조화하여 저장\n
    languages = Column(JSON, nullable=True)  # 언어 정보를 구조화하여 저장\n
    certificates = Column(JSON, nullable=True)  # 자격증 정보를 구조화하여 저장\n
    """

    __tablename__ = "resumes"
    __table_args__ = {
        "schema": "recruitment",
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
    }

    # User 테이블의 id를 기본 키이자 외래 키로 사용
    user_id = Column(String(56),
                     ForeignKey("recruitment.users.id",
                                ondelete='CASCADE', onupdate='CASCADE'),
                     primary_key=True)
    # 실명
    real_name = Column(Text, nullable=True)
    # 지원자 설명
    summary = Column(Text, nullable=True)
    # 기술스택
    skill_stack = Column(JSON, nullable=True)
    # 경력
    # JSON 구조: position, company, work_date, work_description 포함
    work_experiences = Column(JSON, nullable=True)
    # 학위
    # JSON: school_name, degree_date, final_degree, major, gpa
    education = Column(JSON, nullable=True)
    # 교육 및 기타경험
    # JSON: edu_exp, edu_exp_date
    education_and_exp = Column(JSON, nullable=True)
    # 자격증, 수상내역, 언어, 기타 정보
    # JSON: certificate, certificate_date
    certificates = Column(JSON, nullable=True)
    awards = Column(JSON, nullable=True)  # JSON: award, award _date
    languages = Column(JSON, nullable=True)  # JSON: languages, language_date

    # User와의 관계 설정 - 양방향 참조를 위해 수정
    # 역참조 관계 설정 (필수는 아님)
    # table_users = relationship("User", back_populates="table_resumes")


def create_resume(
    db: Session,
    user_id: str,
    real_name: Optional[str] = None,
    summary: Optional[str] = None,
    skill_stack: Optional[List[float]] = None,
    work_experiences: Optional[List[dict]] = None,
    education: Optional[List[dict]] = None,
    education_and_exp: Optional[List[dict]] = None,
    certificates: Optional[List[dict]] = None,
    awards: Optional[List[dict]] = None,
    languages: Optional[List[dict]] = None
):
    resume = Resume(
        user_id=user_id,
        real_name=real_name,
        summary=summary,
        skill_stack=skill_stack,
        work_experiences=work_experiences,
        education=education,
        education_and_exp=education_and_exp,
        certificates=certificates,
        awards=awards,
        languages=languages
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_resume_by_id(db: Session, user_id: str):
    return db.query(Resume).filter(Resume.user_id == user_id).first()


def update_resume(
    db: Session,
    user_id: str,
    real_name: Optional[str] = None,
    summary: Optional[str] = None,
    skill_stack: Optional[List[float]] = None,
    work_experiences: Optional[List[dict]] = None,
    education: Optional[List[dict]] = None,
    education_and_exp: Optional[List[dict]] = None,
    certificates: Optional[List[dict]] = None,
    awards: Optional[List[dict]] = None,
    languages: Optional[List[dict]] = None
):
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    if not resume:
        return None

    updates = {
        "real_name": real_name,
        "summary": summary,
        "skill_stack": skill_stack,
        "work_experiences": work_experiences,
        "education": education,
        "education_and_exp": education_and_exp,
        "certificates": certificates,
        "awards": awards,
        "languages": languages
    }

    for field, value in updates.items():
        if value is not None:
            setattr(resume, field, value)

    db.commit()
    db.refresh(resume)
    return resume


def delete_resume(db: Session, user_id: str):
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    if resume:
        db.delete(resume)
        db.commit()
        return True
    return False
