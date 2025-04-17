from typing import Optional, Tuple, Any
from sqlalchemy.orm import Session

from src.db import Session
from src.logic.user.user_logic import UserLogic
from src.logic.resume.resume_logic import ResumeLogic
from src.logic.assistant.assistant_logic import AssistantLogic, AssistantType
from src.logic.assistant.generate_roadmap_img import split_text_and_json

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

    # ---------------------------------------------------------
    # 기본 로그인/회원가입 구현
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
        self.resume_logic.create_resume(user_id=user_id)

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

    # ---------------------------------------------------------
    # USER 로직
    def get_user_img(self) -> str:
        """사용자 카드 이미지 주소를 반환합니다."""
        return self.user_logic.get_user_img()

    def update_user_resume_file(self, resume_file_url: str) -> None:
        """유저의 이력서 PDF 파일 URL을 User 테이블 DB에 저장합니다."""
        return self.user_logic.update_resume_file(resume_file_url)

    def update_user_wanted(self, wanted_position) -> None:
        """희망직무를 업데이트 합니다. 업데이트 된 경우, 자동으로 새로운 사용자 카드를 만듭니다."""
        return self.user_logic.update_wanted_position(wanted_position)

    # ---------------------------------------------------------
    # RESUME 로직
    def generate_resume_pdf(self):
        """이력서 PDF를 생성합니다."""
        return self.resume_logic.generate_pdf_from_resume_id()

    def update_resume_info(self, resume_fields: dict[str, Any]) -> None:
        """
        사용자 페이지의 resume 입력 정보를 Resume 테이블 DB에 저장합니다.

        Args:
            resume_fields (Dict[str, Any]): 업데이트할 이력서 정보 필드들.
        """
        return self.resume_logic.update_resume_info(resume_fields)

    def reset_resume_info(self) -> None:
        """
        이력서 DB를 초기화합니다.(key값인 user_id 제외)
        - 이력서 지우기 버튼 눌렀을 경우, 실행
        """
        self.resume_logic.reset_resume_info()

    def get_resume_info(self) -> dict:
        """
        이력서 DB를 불러옵니다.
        - 처음 사용자 페이지를 눌렀을 때 v
        - 변경 취소하기 버튼 눌렀을 때 ? 
        - 저장버튼 누른 뒤에도 update_resume_info 실행 후 → 불러와야 함 v
        """
        return self.resume_logic.get_resume_info()

    # ---------------------------------------------------------
    # ASSISTANT 로직
    def get_response_from_assistant(self, assistant_type: AssistantType, user_question: str) -> dict:
        """AI 도우미를 통해 사용자 질문에 응답합니다"""
        response_message = self.assistant_logic.get_response_from_assistant(
            assistant_type, user_question)
        return response_message

    def get_all_thread_dialogue(self, assistant_type: AssistantType) -> dict:
        """사용자의 assistant_type에 해당하는 Thread ID를 통해 전체 대화 내역"""
        return self.assistant_logic.get_all_thread_dialogue(assistant_type)

    def add_dialogue_thread(self, role: str, message: str) -> None:
        """스레드에 해당 역할에 대한 메세지를 추가합니다."""
        return self.assistant_logic.add_dialogue_thread(role, message)

    def delete_update_user_thread_id(self) -> None:
        """
        사용자의 모든 thread_id를 삭제하고 새로 생성합니다.

        Raises:
            RuntimeError: 스레드 삭제 또는 생성 중 문제가 발생할 경우.
        """
        try:
            # 모든 thread_id 삭제
            self.assistant_logic.delete_user_thread_id()
            # 새로운 thread_id 생성
            self.user_logic.update_thread_id()
        except Exception as e:
            raise RuntimeError(f"thread_id 삭제 또는 생성 중 문제가 발생했습니다: {e}")

    def split_roadmap_text_image(self, roadmap_response: str, message_id: str) -> Tuple[str, str]:
        """
        로드맵 응답 데이터를 텍스트와 이미지 경로로 분리합니다.

        Args:
            roadmap_response (str): 로드맵 기능에서 출력된 응답 데이터 (JSON 형식의 문자열).
            message_id (str): message_id

        Returns:
            Tuple[str, str]: 
                - 텍스트 부분 (로드맵 설명).
                - 이미지 경로 (로드맵 이미지 파일 경로).(세로 / 가로)
        """
        roadmap_text, roadmap_image_path = split_text_and_json(
            roadmap_response, user_id=self._user_id, message_id=message_id)
        return roadmap_text, roadmap_image_path

    def extract_citations_to_url(self, response: str) -> list:
        """응답이 선택됐을 때 그 응답에서 url 리스트로 나옴"""
        return self.assistant_logic.extract_citations_url(response)

    # ---------------------------------------------------------
    # DB Session 닫기
    def __del__(self):
        # 인스턴스 소멸 시 세션 닫기
        if hasattr(self, "db"):
            self.db.close()


app_logic = AppLogic()
