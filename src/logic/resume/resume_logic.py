from typing import Optional
from sqlalchemy.orm import Session

from src.models.resume import get_resume_by_id, create_resume, update_resume, delete_resume
from src.logic.resume.generate_pdf_resume import generate_pdf_resume


class ResumeLogic:
    def __init__(self, db: Session, user_id: Optional[str] = None):
        """
        ResumeLogic 클래스 초기화 메서드.

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션.
            user_id (Optional[str]): 초기화 시 설정할 사용자 ID (기본값: None).
        """
        self._signed_in: bool = user_id is not None
        self._user_id: Optional[str] = user_id
        self.db = db

    def update_resume_info(
        self,
        **resume_fields
    ) -> None:
        """
        사용자의 이력 정보를 Resume 테이블에 생성 또는 업데이트합니다.

        Args:
            **resume_fields: 업데이트 또는 생성할 이력 정보 필드들 (None 값은 무시됨)
        """

        existing_resume = get_resume_by_id(self.db, self._user_id)

        # None인 값은 필터링
        filtered_data = {k: v for k,
                         v in resume_fields.items() if v is not None}

        filtered_data["user_id"] = self._user_id

        if existing_resume:
            update_resume(db=self.db, **filtered_data)
        else:
            create_resume(db=self.db, **filtered_data)

    def generate_pdf_from_resume_id(self) -> str:
        """
        사용자의 이력서 정보를 기반으로 PDF 파일을 생성합니다.

        Returns:
            str: 생성된 PDF 파일의 경로

        Raises:
            ValueError: 이력서 정보가 존재하지 않을 경우 예외를 발생시킵니다.
        """
        resume = get_resume_by_id(db=self.db, user_id=self._user_id)
        # 저장 원하는 위치로 수정 가능.
        output_path = r"src/tmp/outputs/resume.pdf"

        if not resume:
            raise ValueError("이력서를 찾을 수 없습니다.")

        # 안전하게 None 처리
        def safe_data(val, default):
            return val if val else default

        user_info = {
            "real_name": resume.real_name or "",
            "summary": resume.summary or "",
            "skill_stack": safe_data(resume.skill_stack, []),
            "work_experiences": safe_data(resume.work_experiences, []),
            "education": safe_data(resume.education, {}),
            "education_and_exp": safe_data(resume.education_and_exp, []),
            "certificates": safe_data(resume.certificates, []),
            "awards": safe_data(resume.awards, []),
            "languages": safe_data(resume.languages, [])
        }
        return generate_pdf_resume(output_path, user_info)
