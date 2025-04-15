class ResumeLogic:
    def update_resume_file(self, resume_file_url: str) -> None:
        """
        유저의 이력서 PDF 파일 URL을 DB에 저장합니다.

        Args:
            db (Session): SQLAlchemy 세션
            resume_file_url (str): 업로드된 PDF 파일 경로 또는 URL

        Returns:
            User: 업데이트된 사용자 객체 또는 None (사용자 미존재 시)
        """

        update_user(
            db=self.db,
            user_id=self._user_id,
            resume_file=resume_file_url,
        )

    def update_resume_info(
        self,
        **resume_fields
    ) -> None:
        """
        사용자의 이력 정보를 Resume 테이블에 생성 또는 업데이트합니다.

        Args:
            **resume_fields: 업데이트 또는 생성할 이력 정보 필드들 (None 값은 무시됨)
        """

        existing_resume = get_resume_by_id(self.db, self._user_id)

        # None인 값은 필터링
        filtered_data = {k: v for k,
                         v in resume_fields.items() if v is not None}

        filtered_data["user_id"] = self._user_id

        if existing_resume:
            update_resume(db=self.db, **filtered_data)
        else:
            create_resume(db=self.db, **filtered_data)

    def generate_pdf_from_resume_id(self) -> str:
        """
        사용자의 이력서 정보를 기반으로 PDF 파일을 생성합니다.

        Returns:
            str: 생성된 PDF 파일의 경로

        Raises:
            ValueError: 이력서 정보가 존재하지 않을 경우 예외를 발생시킵니다.
        """
        resume = get_resume_by_id(db=self.db, user_id=self._user_id)
        # 저장 원하는 위치로 수정 가능.
        output_path = r"src/tmp/outputs/resume.pdf"

        if not resume:
            raise ValueError("이력서를 찾을 수 없습니다.")

        # 안전하게 None 처리
        def safe_data(val, default):
            return val if val else default

        user_info = {
            "real_name": resume.real_name or "",
            "summary": resume.summary or "",
            "skill_stack": safe_data(resume.skill_stack, []),
            "work_experiences": safe_data(resume.work_experiences, []),
            "education": safe_data(resume.education, {}),
            "education_and_exp": safe_data(resume.education_and_exp, []),
            "certificates": safe_data(resume.certificates, []),
            "awards": safe_data(resume.awards, []),
            "languages": safe_data(resume.languages, [])
        }
        return generate_pdf_resume(output_path, user_info)
