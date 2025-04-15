class UserLogic:
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
        from src.models.user import User

        # User 테이블에서 user_id 로 사용자 조회
        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False, "아이디가 존재하지 않습니다."

        if not user.verify_password(password):
            return False, "비밀번호가 틀렸습니다."

        # 로그인 성공
        self._signed_in = True
        self._user_id = user_id
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
        from src.models.user import User

        # 기존 사용자 존재 여부 확인
        existing_user = self.db.query(User).filter(User.id == user_id).first()
        if existing_user:
            return False, "이미 존재하는 아이디입니다."

        # 회원가입 로직 수행
        create_user(self.db, user_id=user_id, password=password)

        self.sign_in(user_id, password)

        self._update_vector_store()
        self._update_thread_id()
        self._update_user_img()

        return True, "회원가입에 성공했습니다."

    def _update_vector_store(self) -> str:
        """DB에서 사용자 가져오고, 벡터 스토어가 없으면 새로 생성해서 DB에 업데이트
        Returns:
            str: 벡터 스토어 ID
        """
        user = get_user_by_id(self.db, user_id=self._user_id)

        if not user:
            raise ValueError(f"User with id {self._user_id} not found")

        if user.vector_store_id:
            pass
            return user.vector_store_id
        else:
            # Azure에서 ID 가져오기
            vector_store_id = get_vector_store(vector_store_name=self._user_id)

            # DB에 업데이트
            update_user(db=self.db, user_id=self._user_id,
                        vector_store_id=vector_store_id)
        return vector_store_id

    def _update_thread_id(self) -> None:
        """
        사용자의 thread_id를 생성한 뒤, 이를 DB에 저장합니다.

        Args:
            db (Session): SQLAlchemy DB 세션
        """
        thread_types = ["assistant", "job_recommend",
                        "recruit_recommend", "roadmap", "resume_review", "find_study"]
        thread_ids = {
            f"thread_id_{thread_type}": create_new_thread(AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY)
            for thread_type in thread_types
        }
        update_user(db=self.db, user_id=self._user_id, **thread_ids)

    def _update_user_img(self, wanted_position: str = '미정') -> None:
        """
        사용자의 직무 정보를 기반으로 아바타 카드 이미지를 생성하고,
        해당 이미지 경로를 DB에 저장합니다.

        Args:
            wanted_position (str): 사용자의 희망 직무 (없을 경우 '미정'으로 처리)
        """

        job = wanted_position if wanted_position else "미정"
        update_user(
            db=self.db,
            user_id=self._user_id,
            user_img=generate_avatar_id_card(seed=self._user_id, job=job),
            wanted_position=job
        )

    def get_user_img(self) -> str:
        """
        사용자의 아바타 카드 이미지 URL을 반환합니다.
        Returns:
            str: 사용자의 user_img URL

        Raises:
            ValueError: 해당 사용자가 존재하지 않을 경우
        """
        user = get_user_by_id(db=self.db, user_id=self._user_id)
        if user is None:
            raise ValueError("해당 사용자가 존재하지 않습니다.")

        return user.user_img

    def _update_wanted_position(
        self, wanted_position: str
    ) -> None:
        """
        사용자의 희망 직무를 DB에 반영하고,
        변경된 직무에 맞춰 아바타 카드 이미지를 새로 생성해 저장합니다.

        Args:
            wanted_position (str): 새로 설정할 희망 직무
        """
        update_user(
            db=self.db,
            user_id=self._user_id,
            wanted_position=wanted_position,
            user_img=generate_avatar_id_card(
                seed=self._user_id, job=wanted_position),
        )
