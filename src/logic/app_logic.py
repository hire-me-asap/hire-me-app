import os
import time

from dotenv import load_dotenv
from typing import Optional, TypedDict
from openai.types import VectorStore
from sqlalchemy.orm import Session

from src.logic.openai_requests import (
    upload_vector_store_files,
    get_vector_store_files_list,
    delete_vector_store_files,
    get_vector_store,
    create_new_thread,
    add_user_question_to_thread,
    run_message_to_thread,
    is_run_done,
    get_last_assistant_message,
)

from src.models.recruitment import get_user_by_id, update_user, create_user, delete_user
from src.models.recruitment import User
from src.logic.generate_id_card import generate_avatar_id_card

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


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
        self.signed_in: bool = False

        self._user_id: Optional[str] = None
        self._vector_store_id: Optional[str] = None

    def upload_user_files(self, *files: str):
        """파일을 사용자 전용 벡터 스토어에 업로드합니다.

        Args:
            *files (str): 업로드할 파일의 경로
        """
        if not self.signed_in:
            raise RuntimeError("로그인 정보가 없습니다.")
        upload_vector_store_files(self._vector_store_id, files)

    def list_user_files(self) -> list[FileInfo]:
        """사용자 전용 벡터 스토어에 업로드된 모든 파일의 ID 리스트를 반환합니다.

        Returns:
            list[FileInfo]: 파일 정보가 담긴 리스트입니다.
        """
        if not self.signed_in:
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
        if not self.signed_in:
            raise RuntimeError("로그인 정보가 없습니다.")

        delete_vector_store_files(
            vector_store_id=self._vector_store_id, file_ids=file_ids
        )

    def sign_in(self, db: Session, user_id: str, password: str) -> bool:
        # User 테이블에서 user_id 로 사용자 조회
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False  # 사용자 없음 → 로그인 실패

        if not user.verify_password(password):
            return False  # 비밀번호 불일치 → 로그인 실패

        # 로그인 성공
        self.username = user.id
        return True

    def sign_up(
        self, db: Session, user_id: str, password: str
    ):  # hashing은 create에서 됨
        existing_useruser = db.query(User).filter(User.id == user_id).first()
        if existing_useruser:
            return "이미 존재하는 아이디입니다."
        else:
            create_user(db, user_id=user_id, password=password)
            self._update_vector_store(db, user_id=user_id)
            self._update_thread_id(db, user_id=user_id)
            self._update_user_img(db, user_id=user_id)
            return True

    def _update_vector_store(self, db: Session, user_id: str) -> str:
        """DB에서 사용자 가져오고, 벡터 스토어가 없으면 새로 생성해서 DB에 업데이트

        Args:
            db (Session): DB 세션
            user_id (str): 사용자 ID

        Returns:
            str: 벡터 스토어 ID
        """
        user = get_user_by_id(db, user_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        if user.vector_store_id:
            pass
            return user.vector_store_id
        else:
            # Azure에서 ID 가져오기
            vector_store_id = get_vector_store(vector_store_name=user_id)

            # DB에 업데이트
            update_user(db=db, user_id=user_id,
                        vector_store_id=vector_store_id)
        return vector_store_id

    # thread_id 생성 후, DB 업데이트
    def _update_thread_id(self, db: Session, user_id: str) -> None:
        job, recruit, roadmap, resume = [
            create_new_thread(AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY)
            for _ in range(4)
        ]

        update_user(
            db=db,
            user_id=user_id,
            thread_id_job_recommend=job,
            thread_id_recruit_recommend=recruit,
            thread_id_roadmap=roadmap,
            thread_id_resume_review=resume,
        )

    # 사용자 정보 카드 이미지 제작 후 경로 DB에 저장
    def _update_user_img(self, db: Session, user_id: str, wanted_position: str) -> None:
        job = wanted_position if wanted_position else "미정"
        update_user(
            db=db,
            user_id=user_id,
            user_img=generate_avatar_id_card(seed=user_id, job=job),
        )

    # 희망직무 업데이트 되었을 때 DB에 업데이트 및 이미지 주소 재설정
    def _update_wanted_position(
        self, db: Session, user_id: str, wanted_position: str
    ) -> None:
        update_user(
            db=db,
            user_id=user_id,
            wanted_position=wanted_position,
            user_img=generate_avatar_id_card(
                seed=user_id, job=wanted_position),
        )

    def assistant_logic(assistant_id, message, thread_id):
        # 1. 사용자 메시지 thread에 추가
        response = add_user_question_to_thread(
            personal_thread_id=thread_id,
            user_question=message
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to add user question to thread: {response.text}")

        # 2. run 실행
        run_id = run_message_to_thread(
            thread_id=thread_id,
            assistant_id=assistant_id,
            message=message
        )
        if not run_id:
            raise Exception("Failed to start run for the thread.")

        polling_interval = 1
        max_wait_time = 30
        # 3. 폴링하면서 run 완료될 때까지 대기
        elapsed_time = 0
        while not is_run_done(thread_id, run_id):
            if elapsed_time >= max_wait_time:
                raise TimeoutError(
                    "Run did not complete within the maximum wait time.")
            time.sleep(polling_interval)
            elapsed_time += polling_interval

        # 4. assistant 응답 가져오기
        response_message = get_last_assistant_message(thread_id)
        return {"status": "completed", "response": response_message}

    
    def get_user_response(user_id, assistant_type, user_question):
        """
        유저 반응 가져오기(assistant_logic 이전)
        """
        # "assistant_type(서비스 5개 중 선택)" : ["assistant_id1", "thread_id"] 
        assistant_mapping = {"a":["assistant_id1", "thread_id_job_recommend"], "b":["assistant_id2", "thread_id_recruit_recommend"], "c":["assistant_id3", "thread_id_roadmap"], "d":["assistant_id4", "thread_id_resume_review"], "e":["assistant_id5", "thread_id_find_study"]}
        
        assistant_info = assistant_mapping[assistant_type]
        assistant_id = assistant_info[0]
        thread_column_name = assistant_info[1]

        # 유저 가져오기 (로그인 후 실행되는 코드)
        user = db.query(User).filter(User.id == user_id).first()

        # 해당 assistant에 맞는 thread_id 필드 가져오기
        personal_thread_id = getattr(user, thread_column_name)

        # 실제 도우미 응답 함수 호출
        return assistant_logic(assistant_id, user_question, personal_thread_id)   