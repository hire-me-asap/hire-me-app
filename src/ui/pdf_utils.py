from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def generate_resume_pdf(user_info):
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))  # 📍템플릿 경로 주의!
    template = env.get_template("resume_template.html")

    # 📌 HTML 렌더링
    html_out = template.render(user_info)
    user_info = {
    "real_name": "홍길동",
    "summary": "엣취~~",
    "work_experiences": [
        {
            "work_date": "2023.01 - 2024.02",
            "company": "ABC Corp",
            "position": "AI 인턴",
            "work_description": ["모델 학습", "데이터 전처리"]
        }
    ],
    "education": [
        {
            "school_name": "서울대학교",
            "degree_date": "2019.03 - 2023.02",
            "final_degree": "학사",
            "gpa": "4.1",
            "major": "경영정보학"
        }
    ],
    "education_and_exp": [
        {"edu_exp": "MS AI School", "edu_exp_date": "2024.01 - 2024.06"}
    ],
    "certificates": [
        {"certificate": "정보처리기사", "certificate_date": "2023.08.01"}
    ],
    "awards": [
        {"award": "AI 경진대회 대상", "award_date": "2023.10.10"}
    ],
    "languages": [
        {"language": "영어", "language_date": "2022.12.10"}
    ]
    }
    # 📌 PDF 생성
    output_path = "resume.pdf"
    HTML(string=html_out).write_pdf(output_path)

    return output_path
