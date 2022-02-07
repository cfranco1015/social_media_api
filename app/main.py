import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi")
from importlib.resources import path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from app.config import settings

# auto generate tables if they fo not exist in PostgreSQL
#models.Base.metadata.create_all(bind = engine)

app = FastAPI()

# changes in code can be seen in browser/postman if the server has been rebooted
# use this command in terminal to have saved changes automatically restart the server:
# uvicorn file:decorator --reload (i.e. uvicorn main:app --reload)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World successfully deployed from CI/CD pipeline "}


# created .gitignore file to exclude which files not to include when uploading to GitHub
# list proejct dependcies in  text file and install them in terminal respectively
# pip freeze > requirements.txt 
# pip install -r requirements.txt 