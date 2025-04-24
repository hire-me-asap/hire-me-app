![Azure](https://img.shields.io/badge/Azure%20OpenAI-%23412991.svg?style=flat&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=flat&logo=mysql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=flat&logo=gunicorn&logoColor=white)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=flat&logo=selenium&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF6F00?style=flat&logo=gradio&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=flat&logo=github&logoColor=white)

[<img align="center" height="60px" src="https://raw.githubusercontent.com/hire-me-asap/.github/main/profile/resources/%EC%97%A3%EC%B7%A8-%ED%83%80%EC%9D%B4%ED%8B%80.png">](#)

🤧 **엣취**는 IT 분야 비기너를 위한 취업 준비를 돕는 **맞춤형 구직 도우미**입니다.

🎯 사용자의 이력서를 **분석**하여 다음 기능을 제공합니다:
- 📝 이력서 피드백
- ✉️ 최신 채용 공고 추천
- 💼 직무 추천
- 🗺️ 성장 로드맵 제시
- 🎓 강의 추천

✨ **이력서 작성**을 돕기 위해 다음의 부가 기능을 제공합니다:
- 🖨️ 이력서를 PDF로 출력
- 🛠️ 요즘 핫한 기술 스택 리스트업

---
# `hire-me-app`
**엣취**의 DB, 백엔드, 프론트엔드 로직이 모두 구현된 레포지토리입니다.

## 🚀 기능

### 🎯 주요 기능:

- 📝 **이력서 피드백**: 사용자가 입력한 이력서 정보를 기반으로 AI가 피드백을 제공합니다. `OpenAI API`를 활용하여 이력서의 개선점을 제안하며, 사용자의 경력과 기술 스택에 맞는 조언을 제공합니다.
- ✉️ **최신 채용 공고 추천**: 사용자의 위치, 기술 스택, 관심 직무를 기반으로 최신 채용 공고를 추천합니다. 데이터베이스와 연동하여 실시간으로 업데이트된 정보를 제공합니다.
- 💼 **직무 추천**: 사용자의 기술 스택과 경력을 분석하여 적합한 직무를 추천합니다. AI 기반 분석을 통해 사용자가 도전할 수 있는 직무를 제안합니다.
- 🗺️ **성장 로드맵 제시**: 사용자의 경력 데이터를 기반으로 `Graphviz`를 활용하여 시각적인 커리어 로드맵 이미지를 생성합니다. 이 로드맵은 사용자가 목표를 설정하고 경력을 계획하는 데 도움을 줍니다.
- 🎓 **강의 추천**: 사용자의 기술 스택과 목표에 맞는 강의를 추천합니다. 최신 트렌드와 관련된 학습 자료를 제공하여 사용자의 역량 강화를 지원합니다.

### ✨ 부가 기능:

- 🖨️ **이력서를 PDF로 출력**: 사용자가 입력한 정보를 바탕으로 PDF 형식의 이력서를 생성합니다. `generate_pdf_resume` 함수는 ReportLab 라이브러리를 사용하여 이력서를 생성하며, 사용자가 다운로드할 수 있도록 제공합니다.
- 🛠️ **요즘 핫한 기술 스택 리스트업**: 프로젝트 내에서 최신 기술 스택 리스트를 관리하며, 사용자가 선택할 수 있도록 UI에 표시합니다. 예를 들어, Python, AWS, Docker와 같은 기술이 포함됩니다.

## 🖥️ 구현 방식

### 1. **데이터베이스 (DB)**

- **SQLAlchemy**와 **Alembic**을 사용하여 데이터베이스 스키마를 관리.
- 사용자 정보, 스레드 ID, 이력서 데이터 등을 저장.
- Alembic을 통해 데이터베이스 마이그레이션을 수행하여 스키마 변경을 관리.

### 2. **백엔드 로직**

- **AI 도우미**: OpenAI API와 통신하여 사용자 질문에 대한 응답 생성.
- **로드맵 생성**: Graphviz를 사용해 커리어 로드맵 이미지를 생성.
- **이력서 생성**: HTML 템플릿을 기반으로 PDF 이력서를 생성.
- **사용자 관리**: 사용자 정보 업데이트 및 ID 카드 생성.

### 3. **프론트엔드 (UI)**

- **Gradio**를 사용하여 사용자 인터페이스 구성.
- 주요 컴포넌트:
  - **사이드바**: 왼쪽 및 오른쪽 사이드바에서 주요 기능 제공.
  - **챗봇**: AI 도우미와의 대화 인터페이스.
  - **로드맵 갤러리**: 생성된 로드맵 이미지를 표시.
  - **이력서 탭**: 사용자 정보를 입력하고 PDF 이력서를 생성.
- **이벤트 핸들러**:
  - 버튼 클릭 및 입력 이벤트를 처리하여 백엔드와 통신.

### 4. **전체 동작 흐름**

1. 사용자가 UI를 통해 입력을 제공.
2. 입력된 데이터는 Gradio 이벤트 핸들러를 통해 백엔드로 전달.
3. 백엔드에서 로직을 처리하고 결과를 반환.
4. 반환된 결과는 Gradio UI에 표시되어 사용자와 상호작용.

## 📂 프로젝트 구조

```
src/
├── logic/
│   ├── assistant/
│   │   ├── assistant_logic.py          # AI 도우미 관련 로직
│   │   ├── generate_roadmap_img.py     # 로드맵 이미지 생성 로직
│   │   ├── openai_requests.py          # OpenAI API 요청 처리
│   ├── resume/
│   │   ├── generate_pdf_resume.py      # 이력서 PDF 생성 로직
│   │   ├── resume_logic.py             # 이력서 관련 로직
│   ├── user/
│   │   ├── generate_id_card.py         # 사용자 ID 카드 생성 로직
│   │   ├── user_logic.py               # 사용자 관련 로직
│   ├── app_logic.py                    # 전체 앱 로직 관리
│   ├── constants.py                    # 상수 정의
├── ui/
│   ├── components/                     # UI 컴포넌트 정의
│   │   ├── chatbot_tab.py              # 챗봇 탭 UI
│   │   ├── profile_tab.py              # 프로필 탭 UI
│   │   ├── left_sidebar.py             # 왼쪽 사이드바 UI
│   │   ├── right_sidebar.py            # 오른쪽 사이드바 UI
│   ├── events/                         # UI 이벤트 핸들러
│   ├── constants.py                    # UI 상수 정의
│   ├── app.py                          # Gradio 앱 초기화 및 컴포넌트 배치
├── migrations/                         # 데이터베이스 마이그레이션 파일
│   ├── versions/                       # Alembic 마이그레이션 버전 관리
```

## ⚙️ 설치 및 실행

### 1. **환경 설정**

```bash
# Python 버전 확인
python --version

# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. **애플리케이션 실행**

```bash
# 애플리케이션 실행
python main.py
```

## 🛠️ 기술 스택

- **프론트엔드**: Gradio
- **백엔드**: Python, FastAPI
- **데이터베이스**: SQLAlchemy, Alembic
- **AI**: OpenAI API
- **PDF 생성**: HTML2PDF
- **이미지 생성**: Graphviz

## 📌 향후 개선 사항

- **UI 개선**:
  - 사용자 경험을 향상시키기 위한 인터페이스 최적화.
- **기능 추가**:
  - 더 많은 AI 기반 추천 기능 추가.
- **성능 최적화**:
  - 대규모 사용자 데이터를 처리할 수 있도록 최적화.

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 배포됩니다.
