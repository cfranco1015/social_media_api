import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi")
from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix= "/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password) # hash user password on database 
    user.password = hashed_password
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
       detail=f"User with id: {id} was not found")
    return user 