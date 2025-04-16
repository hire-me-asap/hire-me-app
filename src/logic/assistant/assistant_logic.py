import time

from enum import Enum
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from src.logic.assistant.openai_requests import (
    add_dialogue_to_thread,
    run_message_to_thread,
    is_run_done,
    get_last_assistant_message_one,
    get_all_assistant_message,
    delete_thread_id,
    get_file_id_name,
)

from src.logic.constants import constants
from src.models.user import User


class AssistantType(Enum):
    JOB_RECOMMEND = "job_recommend"
    RECRUIT_RECOMMEND = "recruit_recommend"
    ROADMAP = "roadmap"
    RESUME_REVIEW = "resume_review"
    FIND_STUDY = "find_study"
    ASSISTANT = "assistant"


class AssistantLogic:
    def __init__(self, db: Session, user_id: Optional[str] = None):
        """
        AssistantLogic 클래스 초기화 메서드.

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션.
            user_id (Optional[str]): 초기화 시 설정할 사용자 ID (기본값: None).
        """
        self._user_id: Optional[str] = user_id
        self.db = db

    def _request_assistant_response(self, assistant_id: str, message: str, thread_id: str) -> str:
        """사용자 질문을 스레드에 추가하고, AI 도우미의 응답을 받아옵니다."""

        # 1. 메시지를 기반으로 도우미 실행(run)
        run_id = run_message_to_thread(
            thread_id=thread_id,
            assistant_id=assistant_id,
            role="user",
            message=message
        )
        if not run_id:
            raise Exception("Failed to start run for the thread.")

        # 2. 도우미가 응답을 완료할 때까지 대기
        polling_interval = 1
        max_wait_time = 30
        elapsed_time = 0
        while not is_run_done(thread_id, run_id):
            if elapsed_time >= max_wait_time:
                raise TimeoutError(
                    "Run did not complete within the maximum wait time.")
            time.sleep(polling_interval)
            elapsed_time += polling_interval

        # 3. 도우미의 최종 응답 메시지 반환
        response = get_last_assistant_message_one(thread_id)

        return response

    def extract_citations(self, response: dict) -> list:
        """
        응답 데이터에서 citations(annotations) 리스트를 추출합니다.

        Args:
            response (dict): OpenAI API의 응답 데이터.

        Returns:
            list: 추출된 citations 리스트.
        """
        citations = response['content'][0]['text']['annotations']

        return citations

    def get_response_from_assistant(
        self, assistant_type: AssistantType, user_question: str
    ) -> Tuple[dict, list]:
        """
        유저 질문을 기반으로 특정 Assistant 타입에 맞는 응답을 반환합니다.

        Args:
            assistant_type (AssistantType): 사용할 도우미 유형(job_recommend, recruit_recommend, roadmap, resume_review, find_study, assistant 중 하나.)
            user_question (str): 유저의 질문 메시지

        Returns:
            dict: 도우미의 응답 메시지 및 참조를 포함한 딕셔너리
        """
        assistant_mapping = {
            AssistantType.ASSISTANT: [constants.ASSISTANT_ID, "thread_id_assistant"],
            AssistantType.JOB_RECOMMEND: [constants.ASSISTANT_ID_JOB_RECOMMEND, "thread_id_job_recommend"],
            AssistantType.RECRUIT_RECOMMEND: [constants.ASSISTANT_ID_RECRUIT_RECOMMEND, "thread_id_recruit_recommend"],
            AssistantType.ROADMAP: [constants.ASSISTANT_ID_ROADMAP, "thread_id_roadmap"],
            AssistantType.RESUME_REVIEW: [constants.ASSISTANT_ID_RESUME_REVIEW, "thread_id_resume_review"],
            AssistantType.FIND_STUDY: [constants.ASSISTANT_ID_FIND_STUDY, "thread_id_find_study"],
        }

        assistant_id, thread_column_name = assistant_mapping[assistant_type]

        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == self._user_id).first()
        personal_thread_id = getattr(user, thread_column_name)

        # 도우미 응답 텍스트 받아오기
        response = self._request_assistant_response(
            assistant_id=assistant_id,
            message=user_question,
            thread_id=personal_thread_id,
        )

        return response

    def get_all_thread_dialogue(self, assistant_type: AssistantType) -> dict:
        """
        사용자의 assistant_type에 해당하는 Thread ID를 통해 전체 대화 내역을 반환합니다.

        Parameters:
            assistant_type (AssistantType): assistant 종류

        Returns:
            dict: 대화 순서를 보장한 전체 메시지 딕셔너리 (role: message)
        """

        user = self.db.query(User).filter(User.id == self._user_id).first()
        if not user:
            raise RuntimeError("사용자를 찾을 수 없습니다.")

        thread_id_map = {
            AssistantType.JOB_RECOMMEND: user.thread_id_job_recommend,
            AssistantType.RECRUIT_RECOMMEND: user.thread_id_recruit_recommend,
            AssistantType.ROADMAP: user.thread_id_roadmap,
            AssistantType.RESUME_REVIEW: user.thread_id_resume_review,
            AssistantType.FIND_STUDY: user.thread_id_find_study,
            AssistantType.ASSISTANT: user.thread_id_assistant,
        }

        thread_id = thread_id_map.get(assistant_type)

        if not thread_id:
            raise RuntimeError(
                "해당 assistant_type에 대한 thread_id가 존재하지 않습니다.", thread_id_map, thread_id)

        message = get_all_assistant_message(thread_id)

        return message

    def add_dialogue_thread(self, role: str, message: str) -> None:

        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == self._user_id).first()
        if not user or not user.thread_id_assistant:
            raise ValueError("유효한 사용자 또는 thread_id_assistant가 없습니다.")

        # 스레드에 대화 추가
        add_dialogue_to_thread(
            personal_thread_id=user.thread_id_assistant,
            role=role,
            message=message
        )

    def delete_user_thread_id(self):
        """
        사용자의 모든 스레드 ID를 삭제합니다.

        Raises:
            ValueError: 유효한 사용자 또는 thread_id_assistant가 없을 경우.
            RuntimeError: 스레드 삭제 중 문제가 발생할 경우.
        """
        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == self._user_id).first()
        if not user or not user.thread_id_assistant:
            raise ValueError("유효한 사용자 또는 thread_id_assistant가 없습니다.")

        # 삭제할 스레드 타입 정의
        thread_types = ["assistant", "job_recommend",
                        "recruit_recommend", "roadmap", "resume_review", "find_study"]

        # 각 스레드 타입에 대한 thread_id 가져오기
        thread_ids = [
            getattr(user, f"thread_id_{thread_type}", None)
            for thread_type in thread_types
        ]

        # 유효한 thread_id만 삭제
        for thread_id in thread_ids:
            if thread_id:
                try:
                    delete_thread_id(thread_id)
                except RuntimeError as e:
                    raise RuntimeError(f"스레드 삭제 중 문제가 발생했습니다: {e}")

    def get_citation_url(self, file_id: str) -> str:
        filename = get_file_id_name(file_id)

        # .txt 제거
        if filename.endswith(".txt"):
            filename = filename[:-4]

        # @를 /로 변환 및 기타 변환
        translation_table = str.maketrans(":/", "!@")  # ':' → '!', '/' → '@'
        citation_url = filename.translate(translation_table)

        return citation_url
