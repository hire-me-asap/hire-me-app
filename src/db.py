import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

# 환경변수 가져오기
DB_DRIVER = os.getenv("SQLALCHEMY_DB_DRIVER", "mysql+pymysql")
DB_USER = os.getenv("SQLALCHEMY_DB_USER")
DB_PASS = quote_plus(os.getenv("SQLALCHEMY_DB_PASS"))  # 특수문자 인코딩
DB_HOST = os.getenv("SQLALCHEMY_DB_HOST")
DB_PORT = os.getenv("SQLALCHEMY_DB_PORT", "3306")
DB_NAME = os.getenv("SQLALCHEMY_DB_NAME")
USE_SSL = os.getenv("SQLALCHEMY_USE_SSL", "False") == "True"
DB_CERT = os.getenv("SQLALCHEMY_DB_CERT")

# SSL 파라미터 구성
ssl_args = ""
if USE_SSL and DB_CERT:
    ssl_args = f"?ssl_ca={DB_CERT}"

# 최종 URL 구성
DATABASE_URL = (
    f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}{ssl_args}"
)

# SQLAlchemy 세션 구성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
