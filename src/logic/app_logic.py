import os
import time
import json

from dotenv import load_dotenv
from typing import List, Optional, TypedDict, Tuple
from openai.types import VectorStore
from sqlalchemy.orm import Session
from enum import Enum

from logic.assistant.openai_requests import (
    upload_vector_store_files,
    get_vector_store_files_list,
    delete_vector_store_files,
    get_vector_store,
    create_new_thread,
    add_dialogue_to_thread,
    run_message_to_thread,
    is_run_done,
    get_last_assistant_message,
    get_all_assistant_response,
    get_assistant_citations,
)

from src.models.user import get_user_by_id, update_user, create_user, delete_user
from src.models.resume import get_resume_by_id, create_resume, update_resume, delete_resume
from logic.user.generate_id_card import generate_avatar_id_card
from logic.resume.generate_pdf_resume import generate_pdf_resume
from src.db import Session


class AssistantType(Enum):
    JOB_RECOMMEND = "job_recommend"
    RECRUIT_RECOMMEND = "recruit_recommend"
    ROADMAP = "roadmap"
    RESUME_REVIEW = "resume_review"
    FIND_STUDY = "find_study"
    ASSISTANT = "assistant"


class FileInfo(TypedDict):
    """벡터 스토어에 업로드된 파일의 정보를 담는 타입입니다.

    Args:
        file_id: 벡터 스토어에 파일을 업로드할 때 지정되는 고유 식별자
        file_name: 원본 파일의 이름
    """

    file_id: str
    file_name: str


class AppLogic:
    """사용자 세션 정보를 관리하고 요청을 처리해주는 클래스입니다.
    한 인스턴스가 한 사용자 세션을 담당합니다.

    Attributes:
        signed_in (str): 사용자가 로그인을 했다면 True, 아니라면 False입니다.
        _user_id (Optional[str]): 사용자가 로그인을 했다면 사용자의 ID가 저장됩니다.
        _vector_store_id (Optional[str]): 사용자가 로그인을 했다면 사용자 전용 벡터 스토어의 ID가 저장됩니다.
    """

    def __init__(self):
        self._signed_in: bool = False
        self._user_id: Optional[str] = None
        self._vector_store_id: Optional[str] = None
        self.db = Session()

    def upload_user_files(self, *files: str):
        """파일을 사용자 전용 벡터 스토어에 업로드합니다.

        Args:
            *files (str): 업로드할 파일의 경로
        """
        if not self._signed_in:
            raise RuntimeError("로그인 정보가 없습니다.")
        upload_vector_store_files(self._vector_store_id, files)

    def list_user_files(self) -> list[FileInfo]:
        """사용자 전용 벡터 스토어에 업로드된 모든 파일의 ID 리스트를 반환합니다.

        Returns:
            list[FileInfo]: 파일 정보가 담긴 리스트입니다.
        """
        if not self._signed_in:
            raise RuntimeError("로그인 정보가 없습니다.")

        files = get_vector_store_files_list(self._vector_store_id)
        files = [FileInfo(file_id=file.id, file_name=file.filename)
                 for file in files]
        return files

    def remove_user_files(self, *file_ids: str) -> bool:
        """파일을 사용자 전용 벡터 스토어에서 삭제합니다.

        Args:
            *files_ids (str): 삭제할 파일의 ID
        """
        if not self._signed_in:
            raise RuntimeError("로그인 정보가 없습니다.")

        delete_vector_store_files(
            vector_store_id=self._vector_store_id, file_ids=file_ids
        )

    def user_id(self):
        """사용자 아이디를 반환합니다.

        Returns:
            str: 사용자 아이디
        """
        if not self._signed_in:
            raise RuntimeError('로그인 정보가 없습니다.')
        return self._user_id

    def signed_in(self):
        """로그인 여부를 반환합니다.

        Returns:
            bool: 로그인 여부
        """
        return self._signed_in

    def __del__(self):
        # 인스턴스 소멸 시 세션 닫기
        if hasattr(self, "db"):
            self.db.close()


app_logic = AppLogic()
