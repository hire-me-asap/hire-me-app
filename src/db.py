import os, sys
from sqlalchemy import (
    URL,
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 프로젝트 루트 경로를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# load_dotenv() 를 config.py 로 옮기고 override=True 를 사용.
# override 를 하지 않으면 .env 파일의 내용을 바꿀 경우 캐싱 문제가 생김.
# load_dotenv()  # .env 파일 로드
from config import Config

# 환경변수 가져오기
# DB_DRIVER = os.getenv("SQLALCHEMY_DB_DRIVER", "mysql+pymysql")
# DB_USER = os.getenv("SQLALCHEMY_DB_USER")
# DB_PASS = quote_plus(os.getenv("SQLALCHEMY_DB_PASS"))  # 특수문자 인코딩
# DB_HOST = os.getenv("SQLALCHEMY_DB_HOST")
# DB_PORT = os.getenv("SQLALCHEMY_DB_PORT", "3306")
# DB_NAME = os.getenv("SQLALCHEMY_DB_NAME")
# USE_SSL = os.getenv("SQLALCHEMY_USE_SSL", "False") == "True"
# DB_CERT = os.getenv("SQLALCHEMY_DB_CERT")

# SSL 파라미터 구성
# ssl_args = ""
# if USE_SSL and DB_CERT:
#     ssl_args = f"?ssl_ca={DB_CERT}"

# 최종 URL 구성
# DATABASE_URL = (
#     f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}{ssl_args}"
# )

# 동작하는 코드 1
DATABASE_URL = Config.SQLALCHEMY_DB_CONN
# print(DATABASE_URL)

connect_args = {
    'charset': 'utf8mb4',
    'init_command': "SET @@collation_connection='utf8mb4_general_ci'"
}

# SQLAlchemy 세션 구성
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=Config.SQLALCHEMY_ECHO)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 동작하는 코드 2
# DATABASE_URL = Config.NON_SSL_CONNECTION
# print(DATABASE_URL)
# connect_args = {
#     'ssl': {'ca': Config.SQLALCHEMY_DB_CERT },
#     'charset': 'utf8mb4',
#     'init_command':"SET @@collation_connection='utf8mb4_general_ci'" # Characterset: utf8mb4
# }
# engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=Config.SQLALCHEMY_ECHO)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    # db = Session()
    # try:
    #     yield db
    # finally:
    #     db.close()

    # finally 안에서 db.close() 외에 다른 작업이 필요하면 위의 코드를 사용하는게 맞음.
    with Session() as db: # 컨텍스트 매니저 사용. 자동으로 db.close() 호출해 줌
        # MySQL 버전 조회
        result = db.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print(f"MySQL 버전: {version}")
    
# 샘플 테스트 코드
# get_db()
