import os
from urllib.parse import quote_plus
# from distutils.util import strtobool
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    DEBUG = False
    TESTING = False
    
    VERSION_NUMBER = "1.2"
    
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DB_DRIVER = os.environ.get('SQLALCHEMY_DB_DRIVER') or 'mysql+pymysql'
    # SQLALCHEMY_USE_SSL = bool(os.environ.get('SQLALCHEMY_USE_SSL', 'False'))
    # SQLALCHEMY_USE_SSL = strtobool(os.environ.get('SQLALCHEMY_USE_SSL', 'False'))
    SQLALCHEMY_USE_SSL = os.environ.get('SQLALCHEMY_USE_SSL', 'False') == 'True'
    SQLALCHEMY_DB_CERT = os.environ.get('SQLALCHEMY_DB_CERT')
    SQLALCHEMY_DB_USER = os.environ.get('SQLALCHEMY_DB_USER', 'user')
    SQLALCHEMY_DB_PASS = quote_plus(os.environ.get('SQLALCHEMY_DB_PASS', 'pass'))
    SQLALCHEMY_DB_HOST = os.environ.get('SQLALCHEMY_DB_HOST', 'localhost')
    SQLALCHEMY_DB_PORT = os.environ.get('SQLALCHEMY_DB_PORT', '3306')
    SQLALCHEMY_DB_NAME = os.environ.get('SQLALCHEMY_DB_NAME', 'dbname')
    
    NON_SSL_CONNECTION = os.environ.get('SQLALCHEMY_DB_CONN') or '{}://{}:{}@{}:{}/{}'.format(
        SQLALCHEMY_DB_DRIVER, SQLALCHEMY_DB_USER, SQLALCHEMY_DB_PASS, SQLALCHEMY_DB_HOST, SQLALCHEMY_DB_PORT, SQLALCHEMY_DB_NAME
    )

    _SSL_CONNECTION = os.environ.get('SQLALCHEMY_DB_CONN') or '{}://{}:{}@{}:{}/{}?ssl_ca={}'.format(
        SQLALCHEMY_DB_DRIVER, SQLALCHEMY_DB_USER, SQLALCHEMY_DB_PASS, SQLALCHEMY_DB_HOST, SQLALCHEMY_DB_PORT, SQLALCHEMY_DB_NAME, SQLALCHEMY_DB_CERT
    )

    SQLALCHEMY_DB_CONN = _SSL_CONNECTION if SQLALCHEMY_USE_SSL and SQLALCHEMY_DB_CERT else NON_SSL_CONNECTION
