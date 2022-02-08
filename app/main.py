import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, user, auth, vote
from app.database import engine
from app import models

# auto generate tables if they do not exist in PostgreSQL
#models.Base.metadata.create_all(bind = engine)

app = FastAPI()

# Set where requests can be sent from, default to wildcard
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

