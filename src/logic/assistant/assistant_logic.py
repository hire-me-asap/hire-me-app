import time

from typing import List, Optional, TypedDict, Tuple
from sqlalchemy.orm import Session
from enum import Enum

from src.logic.assistant.openai_requests import (
    create_new_thread,
    add_dialogue_to_thread,
    run_message_to_thread,
    is_run_done,
    get_last_assistant_message,
    get_all_assistant_response,
    get_assistant_citations,
)


class AssistantType(Enum):
    JOB_RECOMMEND = "job_recommend"
    RECRUIT_RECOMMEND = "recruit_recommend"
    ROADMAP = "roadmap"
    RESUME_REVIEW = "resume_review"
    FIND_STUDY = "find_study"
    ASSISTANT = "assistant"


class AssistantLogic:
    def _request_assistant_response(self, assistant_id: str, message: str, thread_id: str) -> tuple[str, str]:
        """사용자 질문을 스레드에 추가하고, AI 도우미의 응답과 run_id를 받아옵니다."""

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
        response = get_last_assistant_message(thread_id)

        return response, run_id

    def get_response_from_assistant(
        self, assistant_type: AssistantType, user_question: str
    ) -> dict:
        """
        유저 질문을 기반으로 특정 Assistant 타입에 맞는 응답을 반환합니다.

        Args:
            assistant_type (AssistantType): 사용할 도우미 유형(job_recommend, recruit_recommend, roadmap, resume_review, find_study, assistant 중 하나.)
            user_question (str): 유저의 질문 메시지

        Returns:
            dict: 도우미의 응답 메시지를 포함한 딕셔너리
                roadmap일 경우 {"text": str, "image": Image.Image 또는 str}
                그 외에는 {"text": str}
        """
        from src.models.user import User

        assistant_mapping = {
            AssistantType.ASSISTANT: [ASSISTANT_ID, "thread_id_assistant"],
            AssistantType.JOB_RECOMMEND: [ASSISTANT_ID_JOB_RECOMMEND, "thread_id_job_recommend"],
            AssistantType.RECRUIT_RECOMMEND: [ASSISTANT_ID_RECRUIT_RECOMMEND, "thread_id_recruit_recommend"],
            AssistantType.ROADMAP: [ASSISTANT_ID_ROADMAP, "thread_id_roadmap"],
            AssistantType.RESUME_REVIEW: [ASSISTANT_ID_RESUME_REVIEW, "thread_id_resume_review"],
            AssistantType.FIND_STUDY: [ASSISTANT_ID_FIND_STUDY, "thread_id_find_study"],
        }

        assistant_id, thread_column_name = assistant_mapping[assistant_type]

        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == self._user_id).first()
        personal_thread_id = getattr(user, thread_column_name)

        # 도우미 응답 텍스트 받아오기
        response, run_id = self._request_assistant_response(
            assistant_id=assistant_id,
            message=user_question,
            thread_id=personal_thread_id,
        )

        citations = get_assistant_citations(personal_thread_id, run_id)

        response['citations'] = citations
        return response

    def get_all_thread_dialogue(self, assistant_type: AssistantType) -> dict:
        """
        사용자의 assistant_type에 해당하는 Thread ID를 통해 전체 대화 내역을 반환합니다.

        Parameters:
            assistant_type (AssistantType): assistant 종류

        Returns:
            dict: 대화 순서를 보장한 전체 메시지 딕셔너리 (role: message)
        """
        from src.models.user import User

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

        return get_all_assistant_response(thread_id)

    def add_dialogue_thread(self, role: str, message: str) -> None:
        from src.models.user import User

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
