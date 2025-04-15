from enum import Enum

from src.logic.assistant.assistant_logic import AssistantType


class Modes(Enum):
    GENERAL = "general"
    JOB = "job"
    RECRUIT = "recruit"
    RESUME = "resume"
    ROADMAP = "roadmap"
    COURSE = "course"


ASSISTANTS_OF_MODE = {
    Modes.GENERAL: AssistantType.ASSISTANT,
    Modes.JOB: AssistantType.JOB_RECOMMEND,
    Modes.RECRUIT: AssistantType.RECRUIT_RECOMMEND,
    Modes.RESUME: AssistantType.RESUME_REVIEW,
    Modes.ROADMAP: AssistantType.ROADMAP,
    Modes.COURSE: AssistantType.FIND_STUDY,
}

FEATURES = {
    Modes.GENERAL: '무엇이든 물어보세요!',
    Modes.JOB: '직무 찾기',
    Modes.RECRUIT: '채용 공고 찾기',
    Modes.RESUME: '이력서 검토하기',
    Modes.ROADMAP: '취업 준비 로드맵 작성하기',
    Modes.COURSE: '강의 찾기'
}

EXAMPLE_MESSAGES = {
    Modes.GENERAL: [
        {'text': '🐤 신입에게 적합한 직무나 역할이 뭘까?'},
        {'text': '📛 경력이 없어도 도전할 수 있는 직업에는 어떤 것이 있을까?'},
        {'text': '🛠️ 취업 시장에서 인기가 있는 IT 스킬은 뭘까?'},
        {'text': '📝 이력서에 어떤 IT 관련 경험을 추가하면 취업에 유리할까?'},
    ],
    Modes.JOB: [
        {'text': '🐤 신입도 취업할 수 있는 일자리가 있을까?'},
        {'text': '🎨 디자인 관련 지식을 살릴 수 있는 직업에는 뭐가 있을까?'},
        {'text': '💻 프론트엔드에 관한 직업에는 뭐가 있을까?'},
        {'text': '🗄️ 백엔드에 관한 경험이 중요한 직업을 추천해줘'},
        {'text': '🤖 인공지능에 관한 지식을 살릴 수 있는 일자리를 찾아줘'},
    ],
    Modes.RECRUIT: [
        {'text': '📢 지금 지원할 수 있는 신입 개발자 채용 공고를 찾아줘.'},
        {'text': '📍 서울 지역에서 프론트엔드 개발자를 뽑는 공고가 있을까?'},
        {'text': '🏢 백엔드 관련 채용 공고를 알려줘.'},
        {'text': '🐍 Python 기술 스택을 주로 사용하는 회사의 공고를 추천해줘.'},
    ],
    Modes.RESUME: [
        {'text': '📄 내 이력서에서 개선할 점이 있을까?'},
        {'text': '🤔 프로젝트 경험을 이력서에 어떻게 녹여내는 것이 좋을까?'},
        {'text': '✨ 신입 개발자로서 이력서에 어떤 내용을 강조해야 할까?'},
    ],
    Modes.ROADMAP: [
        {'text': '🗺️ 백엔드 개발자가 되기 위한 학습 로드맵을 짜줘.'},
        {'text': '📅 6개월 안에 웹 개발자로 취업하기 위한 계획을 세워줘.'},
        {'text': '📚 비전공자인데 데이터 분석가로 취업하려면 어떤 순서로 공부해야 할까?'},
    ],
    Modes.COURSE: [
        {'text': '🎓 파이썬 기초를 배울 수 있는 온라인 강의를 추천해줘.'},
        {'text': '💻 React 프레임워크 관련해서 평이 좋은 강의가 있을까?'},
        {'text': '💰 무료로 들을 수 있는 데이터베이스 관련 강의를 찾아줘.'},
    ]
}

PROFILE_IMAGE_PLACEHOLDER = 'resources/profile-placeholder.png'
