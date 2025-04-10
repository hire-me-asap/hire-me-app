from typing import Optional, TypedDict

from openai.types import VectorStore
from src.logic.openai_requests import get_vector_store


class VectorStoreFile(TypedDict):
    """벡터 스토어에 업로드된 파일의 정보를 담는 타입입니다.

    Args:
        file_id: 벡터 스토어에 파일을 업로드할 때 지정되는 고유 식별자
        file_name: 원본 파일의 이름
    """
    file_id: str
    file_name: str


class AppLogic:
    def __init__(self):
        self.username: Optional[str] = None
        self.user_vector_store: Optional[VectorStore] = None

    def login(self, username: str, password: str) -> bool:
        """로그인을 시도합니다. 성공하면 True, 아니면 False를 반환합니다.

        Args:
            username (str): 사용자 이름(ID)
            password (str): 암호(비밀번호)

        Returns:
            bool: 로그인 성공 여부
        """
        # TODO: 별도의 사용자 정보 관리 로직으로 변경
        return username.startswith('tester') and password == 'admin'

    def set_username(self, username: str) -> None:
        """사용자 이름을 지정합니다.

        Args:
            username (str): 사용자 이름
        """
        self.username = username

    def load_user_vector_store(self) -> bool:
        """사용자 전용 벡터 스토어를 불러옵니다. 성공하면 True, 아니면 False를 반환합니다.
        사용자 전용 벡터 스토어가 아직 없다면 조용히 새 벡터 스토어를 생성합니다.

        Returns:
            bool: 벡터 스토어 불러오기 성공 여부
        """
        if self.username is None:
            return False

        self.user_vector_store = get_vector_store(self.username)
        return True

    def upload_to_user_vector_store(self, file: str, *files: str) -> bool:
        """파일을 사용자 전용 벡터 스토어에 업로드합니다. 성공하면 True, 아니면 False를 반환합니다.

        Args:
            file (str): 사용자가 업로드한 파일 경로
            *files (str): 추가 파일들

        Returns:
            bool: 업로드 성공 여부
        """
        if self.user_vector_store is None:
            return False

        # IMPL: 업로드 함수가 완성되면 구현
        return True

    def list_user_vector_store(self) -> list[VectorStoreFile]:
        """사용자 전용 벡터 스토어에 업로드된 모든 파일의 ID 리스트를 반환합니다.

        Returns:
            list[VectorStoreFile]: 파일 정보가 담긴 리스트입니다.
        """
        if self.user_vector_store is None:
            raise AttributeError('사용자 전용 벡터 스토어가 없습니다.')

        # IMPL: 조회 함수가 완성되면 구현
        return []

    def remove_from_user_vector_store(self, file_id: str, *file_ids: str) -> bool:
        """파일을 사용자 전용 벡터 스토어에서 삭제합니다. 성공하면 True, 아니면 False를 반환합니다.

        Args:
            file_id (str): 삭제할 파일의 ID
            *files_ids (str): 추가로 삭제할 파일의 ID 

        Returns:
            bool: _description_
        """
        if self.user_vector_store is None:
            return False

        # IMPL: 파일 삭제 기능이 완성되면 구현
        return True
    
    def login(self, db: Session, user_id: str, password: str) -> bool:
       # User 테이블에서 user_id 로 사용자 조회
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False  # 사용자 없음 → 로그인 실패

        if not user.verify_password(password):
            return False  # 비밀번호 불일치 → 로그인 실패

        # 로그인 성공
        self.username = user.id
        return True