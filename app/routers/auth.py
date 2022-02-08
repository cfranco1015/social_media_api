import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi")
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models, schemas, utils, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

# Organize fastapi documentation by tags
router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    #Verify if user exists and correct password was submitted
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Invalid Credentials")

    #create and return access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}