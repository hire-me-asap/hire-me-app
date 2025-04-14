import os
import time
import json

from dotenv import load_dotenv
from typing import List, Optional, TypedDict, Tuple
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
from src.logic.generate_id_card import generate_avatar_id_card
from src.logic.generate_roadmap_img import split_text_and_json
from src.db import Session

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

ASSISTANT_ID = os.getenv("ASSISTANT_ID")
ASSISTANT_ID_JOB_RECOMMEND = os.getenv("ASSISTANT_ID_JOB_RECOMMEND")
ASSISTANT_ID_RECRUIT_RECOMMEND = os.getenv("ASSISTANT_ID_RECRUIT_RECOMMEND")
ASSISTANT_ID_ROADMAP = os.getenv("ASSISTANT_ID_ROADMAP")
ASSISTANT_ID_RESUME_REVIEW = os.getenv("ASSISTANT_ID_RESUME_REVIEW")
ASSISTANT_ID_FIND_STUDY = os.getenv("ASSISTANT_ID_FIND_STUDY")


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
        self.db = Session()

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

    def sign_in(self, user_id: str, password: str) -> Tuple[bool, str]:
        """
        사용자 로그인 기능을 수행합니다.

        Parameters:
            user_id (str): 로그인하려는 사용자의 ID입니다.
            password (str): 로그인하려는 사용자의 비밀번호입니다.

        Returns:
            Tuple[bool, str]: 로그인 성공 여부와 메시지를 반환합니다.
                - (True, "로그인 성공") → 로그인 성공
                - (False, "아이디가 존재하지 않습니다.") → 사용자 없음
                - (False, "비밀번호가 틀렸습니다.") → 비밀번호 불일치
        """
        from src.models.recruitment import User

        # User 테이블에서 user_id 로 사용자 조회
        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False, "아이디가 존재하지 않습니다."

        if not user.verify_password(password):
            return False, "비밀번호가 틀렸습니다."

        # 로그인 성공
        self.username = user.id
        return True, "로그인 성공"

    def sign_up(
        self, user_id: str, password: str
    ) -> Tuple[bool, str]:
        """
        사용자 회원가입 기능을 수행합니다.

        Parameters:
            user_id (str): 새로 등록할 사용자의 ID입니다.
            password (str): 새로 등록할 사용자의 비밀번호입니다.

        Returns:
            Tuple[bool, str]: 회원가입 성공 여부와 메시지를 반환합니다.
                - (True, "회원가입에 성공했습니다.") → 회원가입 성공
                - (False, "이미 존재하는 아이디입니다.") → 아이디 중복
        """
        from src.models.recruitment import User

        # 기존 사용자 존재 여부 확인
        existing_user = self.db.query(User).filter(User.id == user_id).first()
        if existing_user:
            return False, "이미 존재하는 아이디입니다."

        # 회원가입 로직 수행
        create_user(self.db, user_id=user_id, password=password)
        self._update_vector_store(user_id=user_id)
        self._update_thread_id(user_id=user_id)
        self._update_user_img(user_id=user_id)

        return True, "회원가입에 성공했습니다."

    def _update_vector_store(self, user_id: str) -> str:
        """DB에서 사용자 가져오고, 벡터 스토어가 없으면 새로 생성해서 DB에 업데이트

        Args:
            db (Session): DB 세션
            user_id (str): 사용자 ID

        Returns:
            str: 벡터 스토어 ID
        """
        user = get_user_by_id(self.db, user_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        if user.vector_store_id:
            pass
            return user.vector_store_id
        else:
            # Azure에서 ID 가져오기
            vector_store_id = get_vector_store(vector_store_name=user_id)

            # DB에 업데이트
            update_user(db=self.db, user_id=user_id,
                        vector_store_id=vector_store_id)
        return vector_store_id

    def _update_thread_id(self, user_id: str) -> None:
        """
        사용자의 thread_id를 생성한 뒤, 이를 DB에 저장합니다.

        Args:
            db (Session): SQLAlchemy DB 세션
            user_id (str): 업데이트할 사용자 ID
        """
        thread_types = ["job_recommend",
                        "recruit_recommend", "roadmap", "resume_review", "find_study"]
        thread_ids = {
            f"thread_id_{thread_type}": create_new_thread(AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY)
            for thread_type in thread_types
        }
        update_user(db=self.db, user_id=user_id, **thread_ids)

    def _update_user_img(self, user_id: str, wanted_position: str = '미정') -> None:
        """
        사용자의 직무 정보를 기반으로 아바타 카드 이미지를 생성하고,
        해당 이미지 경로를 DB에 저장합니다.

        Args:
            user_id (str): 업데이트할 사용자 ID
            wanted_position (str): 사용자의 희망 직무 (없을 경우 '미정'으로 처리)
        """

        job = wanted_position if wanted_position else "미정"
        update_user(
            db=self.db,
            user_id=user_id,
            user_img=generate_avatar_id_card(seed=user_id, job=job),
            wanted_position=job
        )

    def _update_wanted_position(
        self, user_id: str, wanted_position: str
    ) -> None:
        """
        사용자의 희망 직무를 DB에 반영하고,
        변경된 직무에 맞춰 아바타 카드 이미지를 새로 생성해 저장합니다.

        Args:
            user_id (str): 업데이트할 사용자 ID
            wanted_position (str): 새로 설정할 희망 직무
        """
        update_user(
            db=self.db,
            user_id=user_id,
            wanted_position=wanted_position,
            user_img=generate_avatar_id_card(
                seed=user_id, job=wanted_position),
        )

    # # 스킬 스택 업데이트
    # def update_skill_stack(
    #     self,
    #     user_id: str,
    #     skill_stack: str,
    #     action: str  # 'add' 또는 'remove'
    # ) -> None:
    #     """
    #     사용자의 스킬스택을 추가하거나 제거합니다.

    #     Args:
    #         user_id (str): 사용자 ID
    #         skill_stack (str): 추가 또는 삭제할 스킬
    #         action (str): 'add' 또는 'remove'
    #     """
    #     # 사용자 조회
    #     user = get_user_by_id(db=self.db, user_id=user_id)
    #     if user is None:
    #         raise ValueError("해당 사용자가 존재하지 않습니다.")

    #     # skill_stack 초기화
    #     current_stack = user.skill_stack or []
    #     if isinstance(current_stack, str):
    #         try:
    #             current_stack = json.loads(current_stack)
    #         except json.JSONDecodeError:
    #             current_stack = []

    #     # 액션 처리
    #     if action == "add":
    #         if skill_stack not in current_stack:
    #             current_stack.append(skill_stack)
    #     elif action == "remove":
    #         if skill_stack in current_stack:
    #             current_stack.remove(skill_stack)
    #     else:
    #         raise ValueError("action은 'add' 또는 'remove'만 가능합니다.")

    #     # 업데이트
    #     update_user(
    #         db=self.db,
    #         user_id=user_id,
    #         skill_stack=current_stack
    #     )

    def _request_assistant_response(self, assistant_id: str, message: str, thread_id: str) -> str:
        """사용자 질문을 스레드에 추가하고, AI 도우미의 응답을 받아옵니다.

        Args:
            assistant_id (str): 응답을 요청할 도우미의 ID
            message (str): 사용자의 질문 메시지
            thread_id (str): 사용자의 스레드 ID

        Returns:
            str: 도우미의 응답 메시지 내용
        """
        # 1. 사용자 메시지를 스레드에 추가
        response = add_user_question_to_thread(
            personal_thread_id=thread_id,
            user_question=message
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to add user question to thread: {response.text}")

        # 2. 메시지를 기반으로 도우미 실행(run)
        run_id = run_message_to_thread(
            thread_id=thread_id,
            assistant_id=assistant_id,
            message=message
        )
        if not run_id:
            raise Exception("Failed to start run for the thread.")

        # 3. 도우미가 응답을 완료할 때까지 대기 (최대 30초)
        polling_interval = 1
        max_wait_time = 30
        elapsed_time = 0
        while not is_run_done(thread_id, run_id):
            if elapsed_time >= max_wait_time:
                raise TimeoutError(
                    "Run did not complete within the maximum wait time.")
            time.sleep(polling_interval)
            elapsed_time += polling_interval

        # 4. 도우미의 최종 응답 메시지 반환
        response_message = get_last_assistant_message(thread_id)
        return response_message

    def get_response_from_assistant(
        self, user_id: str, assistant_type: str, user_question: str
    ) -> dict:
        """
        유저 질문을 기반으로 특정 Assistant 타입에 맞는 응답을 반환합니다.

        Args:
            user_id (str): 유저의 ID
            assistant_type (str): 사용할 도우미 유형
            user_question (str): 유저의 질문 메시지

        Returns:
            dict: 도우미의 응답 메시지를 포함한 딕셔너리
                roadmap일 경우 {"text": str, "image": Image.Image 또는 str}
                그 외에는 {"text": str}
        """
        from src.models.recruitment import User

        assistant_mapping = {
            "assistant": [ASSISTANT_ID, "thread_id_assistant"],
            "job_recommend": [ASSISTANT_ID_JOB_RECOMMEND, "thread_id_job_recommend"],
            "recruit_recommend": [ASSISTANT_ID_RECRUIT_RECOMMEND, "thread_id_recruit_recommend"],
            "roadmap": [ASSISTANT_ID_ROADMAP, "thread_id_roadmap"],
            "resume_review": [ASSISTANT_ID_RESUME_REVIEW, "thread_id_resume_review"],
            "find_study": [ASSISTANT_ID_FIND_STUDY, "thread_id_find_study"],
        }

        assistant_id, thread_column_name = assistant_mapping[assistant_type]

        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == user_id).first()
        personal_thread_id = getattr(user, thread_column_name)

        # 도우미 응답 텍스트 받아오기
        response_text = self._request_assistant_response(
            assistant_id=assistant_id,
            message=user_question,
            thread_id=personal_thread_id,
        )

        # 도우미 타입에 따라 처리 방식 다르게
        if assistant_type == "roadmap":
            text, image = split_text_and_json(response_text)
            return {
                "text": text,
                "image": image
            }
        else:
            return {
                "text": response_text
            }

    def upsert_resume_info(
        self,
        user_id: str,
        skill_stack: Optional[List[str]] = None,
        work_experiences: Optional[str] = None,
        final_degree: Optional[str] = None,
        major: Optional[str] = None,
        gpa: Optional[float] = None,
        education_and_exp: Optional[str] = None,
        certificates: Optional[str] = None,
        awards: Optional[str] = None,
        languages: Optional[str] = None,
        additional_info: Optional[str] = None,
    ) -> None:
        """
        사용자의 이력 정보를 Resume 테이블에 생성 또는 업데이트합니다.
        """
        from src.models.resume import (
            get_resume_by_id,
            create_resume,
            update_resume
        )

        existing_resume = get_resume_by_id(self.db, user_id)

        if existing_resume:
            update_resume(
                db=self.db,
                user_id=user_id,
                skill_stack=skill_stack,
                work_experiences=work_experiences,
                final_degree=final_degree,
                major=major,
                gpa=gpa,
                education_and_exp=education_and_exp,
                certificates=certificates,
                awards=awards,
                languages=languages,
                additional_info=additional_info,
            )
        else:
            create_resume(
                db=self.db,
                user_id=user_id,
                skill_stack=skill_stack,
                work_experiences=work_experiences,
                final_degree=final_degree,
                major=major,
                gpa=gpa,
                education_and_exp=education_and_exp,
                certificates=certificates,
                awards=awards,
                languages=languages,
                additional_info=additional_info,
            )

    # TODO : 사용자페이지에서 입력받은 이력서 PDF로 뽑기 -> 형식 고정되어서 출력해야 하나? 권아님

    def __del__(self):
        # 인스턴스 소멸 시 세션 닫기
        if hasattr(self, "db"):
            self.db.close()
