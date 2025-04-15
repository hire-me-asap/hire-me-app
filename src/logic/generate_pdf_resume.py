from sqlalchemy.orm import Session
from src.models.resume import get_resume_by_id, Resume

# TODO wkhtmltopdf + python-pdfkit 사용해서 html을 pdf로 변환할 수 있음.


def generate_resume_pdf(user_info):
    return ""


# DB에서 데이터 가져와서 pdf로 만드는 함수(pdf로 만드는 함수는 위에서 구현예정)
def generate_pdf_from_resume_id(db: Session, resume_id: str) -> str:
    resume: Resume = get_resume_by_id(db, resume_id)
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

    return generate_resume_pdf(user_info)
