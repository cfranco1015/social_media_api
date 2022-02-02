import sys
sys.path.append("/home/christian/Environments/social_media_api/fastapi/app")
from app import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from typing import List, Optional

# path length reduced by using prefix arguement
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# path operation or route
# HTTP GET method : used to retrieve data
# @name --> decorator --> extends orginal functionality of code 

# limit skip and search represent query parameters for URL 
# i.e. http:/localhost:port/posts?limit=2&skip=3&search=word

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# don't need f string when using Pydantic object, where it can be converted into a dictonary using post.dict()
# alos don't use f string to avoid SQL injection for cursor exectuion
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit() # pushes changes to database

    # unpack post fields using **
    new_post = models.Post(owner_id = current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get one single post
# id -- > path parameter
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user))  :
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()
    # return 404 HTTP response status code for unfound id 
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
       detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute(
    #    """DELETE FROM posts WHERE id = %s RETURNING *""",
    #    (str(id),))
    #deleted_post = cursor.fetchone() 
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
       detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
       detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute(
    #    """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #    (post.title, post.content, post.published, str(id))
    #    )
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
       detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
       detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
