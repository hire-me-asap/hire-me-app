from typing import Optional, TypedDict

from openai.types import VectorStore
from src.logic.openai_requests import upload_vector_store_files, get_vector_store_files_list, delete_vector_store_files


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
            raise RuntimeError('로그인 정보가 없습니다.')
        upload_vector_store_files(self._vector_store_id, files)

    def list_user_files(self) -> list[FileInfo]:
        """사용자 전용 벡터 스토어에 업로드된 모든 파일의 ID 리스트를 반환합니다.

        Returns:
            list[FileInfo]: 파일 정보가 담긴 리스트입니다.
        """
        if not self.signed_in:
            raise RuntimeError('로그인 정보가 없습니다.')

        files = get_vector_store_files_list(self._vector_store_id)
        files = [FileInfo(file_id=file.id, file_name=file.filename) for file in files]
        return files

    def remove_user_files(self, *file_ids: str) -> bool:
        """파일을 사용자 전용 벡터 스토어에서 삭제합니다.

        Args:
            *files_ids (str): 삭제할 파일의 ID 
        """
        if not self.signed_in:
            raise RuntimeError('로그인 정보가 없습니다.')

        delete_vector_store_files(vector_store_id=self._vector_store_id, file_ids=file_ids)
    
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

    # 회원가입 함수
    from src.models.recruitment import create_user

    def sign_up(db: Session, user_id: str, password: str): # hashing은 create에서 됨
        existing_useruser = db.query(User).filter(User.id == user_id).first()
        if existing_useruser:
            return "이미 존재하는 아이디입니다."
        else:
            create_user(db, user_id=user_id, password=password)
            return True