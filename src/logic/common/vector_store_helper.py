from src.logic.common.constants import Constants


class VectorStoreHelper:
    def get_vector_store(vector_store_name: str) -> str:
        """이름으로 기존 벡터 스토어를 찾아 ID를 반환합니다.
        존재하지 않는 경우, 새로 생성하여 ID를 반환합니다.

        Args:
            vector_store_name (str): 벡터 스토어 이름 (보통 user_id)

        Returns:
            str: 벡터 스토어의 ID
        """
        for vector_store in Constants.AZURE_OPENAI_CLIENT.vector_stores.list():
            if vector_store.name == vector_store_name:
                return vector_store.id

        new_vector_store = AZURE_OPENAI_CLIENT.vector_stores.create(
            name=vector_store_name)
        return new_vector_store.id

    def get_vector_store_files_list(vector_store_id: str) -> list[FileObject]:
        """벡터 스토어에서 파일 목록을 가져오는 함수 추가
        Args:
            vector_store_id (str): 벡터 스토어 ID

        Returns:
            list[FileObject]: 벡터 스토어의 파일 목록
        """
        vector_store_files = AZURE_OPENAI_CLIENT.vector_stores.files.list(
            vector_store_id=vector_store_id
        ).data
        file_ids = [file.id for file in vector_store_files]
        files = [AZURE_OPENAI_CLIENT.files.retrieve(
            file_id) for file_id in file_ids]
        return files

    def upload_vector_store_files(vector_store_id: str, files: tuple[str]):
        """벡터 스토어에 파일 업로드하는 함수 추가
        Args:
            vector_store_id (str): 벡터 스토어 ID
            files (tuple[str]): 업로드할 파일 경로가 담긴 튜플
        """
        AZURE_OPENAI_CLIENT.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id, files=[
                open(file, mode="rb") for file in files]
        )

    def delete_vector_store_files(vector_store_id: str, file_ids: tuple[str]):
        """벡터 스토어에서 파일 삭제

        Args:
            vector_store_id (str): 벡터 스토어 ID
            file_ids (tuple[str]): 삭제할 파일 아이디들이 담긴 튜플
        """
        for file_id in file_ids:
            AZURE_OPENAI_CLIENT.vector_stores.files.delete(
                vector_store_id=vector_store_id, file_id=file_id
            )
