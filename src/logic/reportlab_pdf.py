from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import inch

# Malgun Gothic 폰트 등록 (경로는 raw string으로 처리)
pdfmetrics.registerFont(TTFont('MalgunGothic', r'C:\Windows\Fonts\malgun.ttf'))

# 기본 스타일 가져오기
styles = getSampleStyleSheet()

# 'Korean' 스타일을 동적으로 추가
korean_style = ParagraphStyle(
    name='Korean',
    fontName='MalgunGothic',
    fontSize=12,
    leading=15,
    spaceAfter=10
)

# 스타일을 추가 (add() 메서드를 사용)
styles.add(korean_style)

# 예시 내용
user_info = {
    'real_name': 'Park',
    'summary': 'AI 분야에 열정을 가진 신입 개발자입니다. 머신러닝과 딥러닝을 활용한 프로젝트 경험이 있으며, 팀워크와 커뮤니케이션 능력을 갖추고 있습니다.',
    'skill_stack': ['Python', 'Pytorch', 'PaddleOCR', 'Azure ML']
}

# PDF 생성 함수


def create_resume_pdf(output_path=r"src\ui\outputs\resume.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=20,
                            leftMargin=20, topMargin=20, bottomMargin=20)
    story = []

    # 제목
    story.append(
        Paragraph(f"<b>{user_info['real_name']}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # 요약
    story.append(
        Paragraph(f"<b>요약</b><br/>{user_info['summary']}", styles["Korean"]))
    story.append(Spacer(1, 12))

    # 기술 스택
    skills = ", ".join(user_info['skill_stack'])
    story.append(Paragraph(f"<b>기술 스택</b><br/>{skills}", styles["Korean"]))
    story.append(Spacer(1, 12))

    # PDF 만들기
    doc.build(story)
    print(f"✅ PDF 저장 완료: {output_path}")


# PDF 생성 호출
if __name__ == "__main__":
    create_resume_pdf()
