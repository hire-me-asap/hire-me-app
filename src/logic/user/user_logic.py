from typing import Optional, Tuple
from sqlalchemy.orm import Session

from src.logic.assistant.openai_requests import create_new_thread
from src.logic.user.generate_id_card import generate_avatar_id_card
from src.models.user import get_user_by_id, update_user, create_user, delete_user

from src.models.user import User


class UserLogic:
    def __init__(self, db: Session, user_id: Optional[str] = None):
        """
        UserLogic 클래스 초기화 메서드.

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션.
            user_id (Optional[str]): 초기화 시 설정할 사용자 ID (기본값: None).
        """
        self._user_id: Optional[str] = user_id
        self.db = db

    def update_thread_id(self) -> None:
        """
        사용자의 thread_id를 생성한 뒤, 이를 DB에 저장합니다.

        Args:
            db (Session): SQLAlchemy DB 세션
        """
        thread_types = ["assistant", "job_recommend",
                        "recruit_recommend", "roadmap", "resume_review", "find_study"]
        thread_ids = {
            f"thread_id_{thread_type}": create_new_thread()
            for thread_type in thread_types
        }
        update_user(db=self.db, user_id=self._user_id, **thread_ids)

    def update_user_img(self, wanted_position: str = '미정') -> None:
        """
        사용자의 직무 정보를 기반으로 아바타 카드 이미지를 생성하고,
        해당 이미지 경로를 DB에 저장합니다.

        Args:
            wanted_position (str): 사용자의 희망 직무 (없을 경우 '미정'으로 처리)
        """

        job = wanted_position if wanted_position else "미정"
        update_user(
            db=self.db,
            user_id=self._user_id,
            user_img=generate_avatar_id_card(seed=self._user_id, job=job),
            wanted_position=job
        )

    def get_user_img(self) -> str:
        """
        사용자의 아바타 카드 이미지 URL을 반환합니다.
        Returns:
            str: 사용자의 user_img URL

        Raises:
            ValueError: 해당 사용자가 존재하지 않을 경우
        """
        user = get_user_by_id(db=self.db, user_id=self._user_id)
        if user is None:
            raise ValueError("해당 사용자가 존재하지 않습니다.")

        return user.user_img

    def update_wanted_position(
        self, wanted_position: str
    ) -> None:
        """
        사용자의 희망 직무를 DB에 반영하고,
        변경된 직무에 맞춰 아바타 카드 이미지를 새로 생성해 저장합니다.

        Args:
            wanted_position (str): 새로 설정할 희망 직무
        """
        update_user(
            db=self.db,
            user_id=self._user_id,
            wanted_position=wanted_position,
            user_img=generate_avatar_id_card(
                seed=self._user_id, job=wanted_position),
        )

    def update_resume_file(self, resume_file_url: str) -> None:
        """
        유저의 이력서 PDF 파일 URL을 User 테이블 DB에 저장합니다.

        Args:
            db (Session): SQLAlchemy 세션
            resume_file_url (str): 업로드된 PDF 파일 경로 또는 URL

        Returns:
            User: 업데이트된 사용자 객체 또는 None (사용자 미존재 시)
        """

        update_user(
            db=self.db,
            user_id=self._user_id,
            resume_file=resume_file_url,
        )
