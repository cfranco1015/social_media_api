import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi")
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# create a new session per request, use the same session through all the request
# and then close it after the request is complete.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
