from pydantic import BaseSettings
import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi")

class Settings(BaseSettings):
  database_hostname: str
  database_port: str
  database_password: str
  database_name: str
  database_username: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int

  class Config:
      env_file = "/home/christian/Environments/social_media_api/fastapi/.env"

settings = Settings()