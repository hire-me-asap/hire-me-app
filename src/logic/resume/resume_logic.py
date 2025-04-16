from typing import Optional
from sqlalchemy.orm import Session

from src.models.resume import get_resume_by_id, create_resume, update_resume, delete_resume, reset_resume
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

    def create_resume(
        self,
        user_id: str
    ) -> None:
        """
        사용자의 이력 정보를 Resume 테이블에 생성합니다.

        Args:
            user_id (str): 생성할 사용자의 ID.
        """
        existing_resume = get_resume_by_id(db=self.db, user_id=self._user_id)

        if existing_resume:
            raise ValueError("이미 존재하는 이력서가 있습니다. 새로 생성할 수 없습니다.")

        # 기본값으로 None 설정
        create_resume(
            db=self.db,
            user_id=user_id,
            real_name=None,
            summary=None,
            skill_stack=None,
            work_experiences=None,
            education=None,
            education_and_exp=None,
            certificates=None,
            awards=None,
            languages=None
        )

    def get_resume_info(self) -> dict:
        """
        resume 테이블의 정보를 불러옵니다.

        Returns:
            dict: 이력서 정보가 담긴 딕셔너리.

        Raises:
            ValueError: 해당 사용자의 이력서가 존재하지 않을 경우.
        """
        # 이력서 정보 조회
        resume = get_resume_by_id(db=self.db, user_id=self._user_id)
        

        # if not resume:
        #     return False

        # 이력서 정보를 딕셔너리로 반환
        return {
            "real_name": resume.real_name,
            "summary": resume.summary,
            "skill_stack": resume.skill_stack,
            "work_experiences": resume.work_experiences,
            "education": resume.education,
            "education_and_exp": resume.education_and_exp,
            "certificates": resume.certificates,
            "awards": resume.awards,
            "languages": resume.languages
        }

    def update_resume_info(
        self,
        resume_fields
    ) -> None:
        """
        사용자의 이력 정보를 Resume 테이블에 업데이트합니다.

        Args:
            **resume_fields: 업데이트할 이력 정보 필드들 (None 값은 무시됨)
        """
        existing_resume = get_resume_by_id(db=self.db, user_id=self._user_id)

        if not existing_resume:
            create_resume(self._user_id)

        # None인 값은 필터링
        filtered_data = {k: v for k,
                         v in resume_fields.items() if v is not None}
        filtered_data["user_id"] = self._user_id

        update_resume(db=self.db, **filtered_data)

    def reset_resume_info(self):
        """
        사용자의 이력서 데이터를 초기화합니다.

        Returns:
            Resume: 초기화된 이력서 객체.

        Raises:
            ValueError: 해당 사용자의 이력서가 존재하지 않을 경우.
        """
        try:
            reset_resume(db=self.db, user_id=self._user_id)
        except ValueError as e:
            print(f"❌ 이력서 초기화에 실패했습니다. (user_id: {self._user_id}): {e}")
            raise

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
        user_id = self._user_id
        output_path = f"static/pdf/{user_id}_resume.pdf"

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
        generate_pdf_resume(output_path, user_info)
        return output_path
