from typing import Optional, TypedDict, Tuple
from sqlalchemy.orm import Session

from src.db import Session
from src.logic.user.user_logic import UserLogic
from src.logic.resume.resume_logic import ResumeLogic
from src.logic.assistant.assistant_logic import AssistantLogic, AssistantType

from src.models.user import create_user
from src.models.user import User


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
        self.db = Session()

        # 각 로직 클래스 초기화
        self.user_logic = UserLogic(self.db, self._user_id)
        self.resume_logic = ResumeLogic(self.db, self._user_id)
        self.assistant_logic = AssistantLogic(self.db, self._user_id)

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

        # User 테이블에서 user_id 로 사용자 조회
        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False, "아이디가 존재하지 않습니다."

        if not user.verify_password(password):
            return False, "비밀번호가 틀렸습니다."

        # 로그인 성공
        self._signed_in = True
        self._user_id = user_id

        self.user_logic = UserLogic(self.db, self._user_id)
        self.resume_logic = ResumeLogic(self.db, self._user_id)
        self.assistant_logic = AssistantLogic(self.db, self._user_id)
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
        # 기존 사용자 존재 여부 확인
        existing_user = self.db.query(User).filter(User.id == user_id).first()
        if existing_user:
            return False, "이미 존재하는 아이디입니다."

        # 회원가입 로직 수행
        create_user(self.db, user_id=user_id, password=password)

        self.sign_in(user_id, password)
        self.user_logic.update_thread_id()
        self.user_logic.update_user_img()

        return True, "회원가입에 성공했습니다."

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

    def get_user_img(self):
        """사용자 카드 이미지 주소를 반환합니다."""
        return self.user_logic.get_user_img()

    def generate_resume_pdf(self):
        """이력서 PDF를 생성합니다."""
        return self.resume_logic.generate_pdf_from_resume_id()

    def get_response_from_assistant(self, assistant_type: AssistantType, user_question: str) -> dict:
        """AI 도우미를 통해 사용자 질문에 응답합니다."""
        return self.assistant_logic.get_response_from_assistant(assistant_type, user_question)

    def get_all_thread_dialogue(self, assistant_type: AssistantType):
        """사용자의 assistant_type에 해당하는 Thread ID를 통해 전체 대화 내역을 반환합니다."""
        return self.assistant_logic.get_all_thread_dialogue(assistant_type)

    def add_dialogue_thread(self, role: str, message: str):
        """스레드에 해당 역할에 대한 메세지를 추가합니다."""
        return self.assistant_logic.add_dialogue_thread(role, message)

    def update_resume_file(self, resume_file_url: str):
        """유저의 이력서 PDF 파일 URL을 User 테이블 DB에 저장합니다."""
        return self.user_logic.update_resume_file(resume_file_url)

    def __del__(self):
        # 인스턴스 소멸 시 세션 닫기
        if hasattr(self, "db"):
            self.db.close()


app_logic = AppLogic()
