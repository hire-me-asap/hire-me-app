from sqlalchemy.orm import Session
from src.models.resume import get_resume_by_id, Resume

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm

# Malgun Gothic 폰트 등록.
# 이것도 아마 폰트 추가하거나 하는 게 있을 것 같은데 한번 찾아보세요.
pdfmetrics.registerFont(TTFont('MalgunGothic', r'C:\Windows\Fonts\malgun.ttf'))

# 사용자 정보 <- 이런 식으로 들어오니까 디자인할 때 참고용으로 계속 둘게요.
# user_info_use = {
#     "real_name": "홍길동",
#     "summary": "AI 분야에 열정을 가진 신입 개발자입니다. 머신러닝과 딥러닝을 활용한 프로젝트 경험이 있으며, 팀워크와 커뮤니케이션 능력을 갖추고 있습니다.",
#     "skill_stack": ["Python", "Pytorch", "PaddleOCR", "Azure ML"],
#     "work_experiences": [
#         {
#             "work_date": "2023.01 - 2024.02",
#             "company": "ABC Corp",
#             "position": "AI 인턴",
#             "work_description": ["모델 학습", "데이터 전처리"]
#         }
#     ],
#     "education": [
#         {
#             "school_name": "서울대학교",
#             "degree_date": "2019.03 - 2023.02",
#             "final_degree": "학사",
#             "major": "경영정보학",
#             "gpa": "4.1"
#         }
#     ],
#     "education_and_exp": [
#         {"edu_exp": "MS AI School", "edu_exp_date": "2024.01 - 2024.06"}
#     ],
#     "certificates": [
#         {"certificate": "정보처리기사", "certificate_date": "2023.08.01"}
#     ],
#     "awards": [
#         {"award": "AI 경진대회 대상", "award_date": "2023.10.10"}
#     ],
#     "languages": [
#         {"language": "영어", "language_date": "2022.12.10"}
#     ]
# }

# PDF 생성 함수


def generate_pdf_resume(output_path: str, user_info: dict):
    """
    주어진 사용자 정보를 바탕으로 이력서 PDF를 생성하는 함수.

    이 함수는 `user_info` 딕셔너리에서 사용자의 이름, 요약, 기술 스택, 경력, 학력, 교육 이수 및 기타 경험,
    자격증, 수상 이력, 언어 능력 등을 추출하여 PDF 형식으로 저장합니다. PDF의 스타일은 `MalgunGothic` 폰트를 사용하여
    다양한 제목과 본문 스타일을 적용합니다.

    매개변수:
    - output_path (str): 생성된 PDF를 저장할 경로. 예를 들어, "resume.pdf".
    - user_info (dict): 이력서 정보를 담고 있는 딕셔너리. 필수 키는 'real_name', 'summary', 'skill_stack' 등입니다.
      예시:
      {
          'real_name': '홍길동',
          'summary': 'AI 분야에 열정을 가진 신입 개발자입니다.',
          'skill_stack': ['Python', 'Pytorch', 'Azure ML'],
          'work_experiences': [{'work_date': '2023.01 - 2024.02', 'company': 'ABC Corp', 'position': 'AI 인턴', 'work_description': ['모델 학습', '데이터 전처리']}],
          ...
      }

    반환값:
    없음. 함수는 PDF 파일을 지정된 경로에 저장합니다.

    예외:
    - user_info에 필요한 필드가 부족할 경우, 이력서 생성에 실패할 수 있습니다.
    """

    # PDF 문서 생성 설정
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()

    # 제목 스타일 정의
    styles.add(ParagraphStyle(name='TitleKorean',
                              fontName='MalgunGothic',
                              fontSize=20,
                              leading=24,
                              spaceAfter=14,
                              alignment=TA_LEFT))

    # 소제목 스타일 정의
    styles.add(ParagraphStyle(name='SubtitleKorean',
                              fontName='MalgunGothic',
                              fontSize=14,
                              leading=18,
                              spaceAfter=8,
                              spaceBefore=12))

    # 본문 스타일 정의
    styles.add(ParagraphStyle(name='NormalKorean',
                              fontName='MalgunGothic',
                              fontSize=11,
                              leading=15,
                              spaceAfter=4))

    story = []

    # 이름 추가 (제목)
    story.append(Paragraph(user_info['real_name'], styles['TitleKorean']))

    # 요약 추가 (소제목 + 본문)
    story.append(Paragraph("요약", styles['SubtitleKorean']))
    story.append(Paragraph(user_info['summary'], styles['NormalKorean']))

    # 기술 스택 추가 (소제목 + 본문)
    story.append(Paragraph("기술 스택", styles['SubtitleKorean']))
    skills = ", ".join(user_info['skill_stack'])
    story.append(Paragraph(skills, styles['NormalKorean']))

    # 경력 추가 (소제목 + 본문)
    if user_info['work_experiences']:
        story.append(Paragraph("경력", styles['SubtitleKorean']))
        for exp in user_info['work_experiences']:
            story.append(Paragraph(
                f"{exp['work_date']} - {exp['company']} ({exp['position']})", styles['NormalKorean']))
            for task in exp['work_description']:
                story.append(Paragraph(f"- {task}", styles['NormalKorean']))

    # 학력 추가 (소제목 + 본문)
    if user_info['education']:
        story.append(Paragraph("학력", styles['SubtitleKorean']))
        for edu in user_info['education']:
            story.append(Paragraph(
                f"{edu['degree_date']} - {edu['school_name']} ({edu['final_degree']}, {edu['major']}, GPA: {edu['gpa']})", styles['NormalKorean']))

    # 교육 이수 및 기타 경험 추가 (소제목 + 본문)
    if user_info['education_and_exp']:
        story.append(Paragraph("교육 이수 및 기타 경험", styles['SubtitleKorean']))
        for edu_exp in user_info['education_and_exp']:
            story.append(Paragraph(
                f"{edu_exp['edu_exp_date']} - {edu_exp['edu_exp']}", styles['NormalKorean']))

    # 자격증 추가 (소제목 + 본문)
    if user_info['certificates']:
        story.append(Paragraph("자격증", styles['SubtitleKorean']))
        for cert in user_info['certificates']:
            story.append(Paragraph(
                f"{cert['certificate_date']} - {cert['certificate']}", styles['NormalKorean']))

    # 수상 이력 추가 (소제목 + 본문)
    if user_info['awards']:
        story.append(Paragraph("수상 이력", styles['SubtitleKorean']))
        for award in user_info['awards']:
            story.append(
                Paragraph(f"{award['award_date']} - {award['award']}", styles['NormalKorean']))

    # 언어 능력 추가 (소제목 + 본문)
    if user_info['languages']:
        story.append(Paragraph("언어 능력", styles['SubtitleKorean']))
        for lang in user_info['languages']:
            story.append(Paragraph(
                f"{lang['language_date']} - {lang['language']}", styles['NormalKorean']))

    # PDF 빌드
    doc.build(story)
    # PDF 저장 완료 로그
    # print(f"✅ PDF 저장 완료: {output_path}")
